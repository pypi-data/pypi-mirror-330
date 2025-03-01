import pytest
import importlib
from ..output import parse_output

class StandardOutputAPIViolationError(Exception):
    pass

@pytest.fixture(scope="session")
def module_name(pytestconfig):
    return pytestconfig.getoption("module_name")

def test_output_type_is_api_dataclass(module_name):
    api_pkg = importlib.import_module(f'core_evals.{module_name}.api_dataclasses')
    parsed_output = parse_output("/workspace/results")
    if not isinstance(parsed_output, api_pkg.EvaluationResult):
        raise StandardOutputAPIViolationError(f"Expected output to be of instance EvaluationResult but returned {type(parsed_output)}")
