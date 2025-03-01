import time
import os

try:
    import requests
    import werkzeug

    from flask import Flask, Response, request
except ImportError:
    raise ImportError("Please install requests, werkzeug, and flask to use the adapter! pip install requests werkzeug flask")


nvcf_adapter = Flask(__name__)

def handle_connection(target_url: str):
    response = requests.request(
        method=request.method,
        url=target_url,
        headers={k:v for k,v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    if response.status_code == 202:
        fetch_retry_count = 0
        delay_seconds = 0.2
        multiplier = 1

        while response.status_code == 202 and fetch_retry_count <= nvcf_adapter.config["FETCH_RETRIES"]:
            request_id = response.headers.get("NVCF-REQID")

            headers={
                "Authorization": request.headers.get("Authorization"),
                "Content-Type": "application/json",
            }
            if "NVCF-POLL-SECONDS" in request.headers:
                headers["NVCF-POLL-SECONDS"] = request.headers.get("NVCF-POLL-SECONDS")

            response = requests.get(
                url=f'{nvcf_adapter.config["STATUS_URL"]}/{request_id}',
                headers=headers,
            )

            time.sleep(delay_seconds * multiplier)
            multiplier *= 2
            fetch_retry_count += 1


        if fetch_retry_count > nvcf_adapter.config["FETCH_RETRIES"]:
            return Response("Request timed out", 408)


    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection'] 
    headers          = [
        (k,v) for k,v in response.raw.headers.items()
        if k.lower() not in excluded_headers
    ]

    response = Response(response.content, response.status_code, headers)
    return response

@nvcf_adapter.route('/', defaults={'path': ''}, methods=["POST"])
@nvcf_adapter.route('/<path:path>', methods=["POST"])
def nvcf_endpoint_handler(path):
    target_url = nvcf_adapter.config["API_URL"]

    return handle_connection(target_url)

def run_adapter(api_url):
    nvcf_adapter.config.update(
        API_URL=api_url,
        STATUS_URL=os.environ.get("NVCF_STATUS_URL", "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status"),
        FETCH_RETRIES=os.environ.get("NVCF_FETCH_RETRIES", 10000),
    )
    werkzeug.serving.run_simple("localhost", 3825, nvcf_adapter, threaded=True)
