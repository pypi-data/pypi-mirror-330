import subprocess
import pytest
from pathlib import Path
import re
import dp_wizard


tests = {
    "flake8 linting": "flake8 . --count --show-source --statistics",
    "pyright type checking": "pyright",
}


@pytest.mark.parametrize("cmd", tests.values(), ids=tests.keys())
def test_subprocess(cmd: str):
    result = subprocess.run(cmd, shell=True)
    assert result.returncode == 0, f'"{cmd}" failed'


def test_version():
    assert re.match(r"\d+\.\d+\.\d+", dp_wizard.__version__)


@pytest.mark.parametrize(
    "rel_path",
    [
        "pyproject.toml",
        "requirements-dev.in",
        "requirements-dev.txt",
        "dp_wizard/utils/code_generators/__init__.py",
    ],
)
def test_opendp_pin(rel_path):
    root = Path(__file__).parent.parent
    opendp_lines = [
        line for line in (root / rel_path).read_text().splitlines() if "opendp[" in line
    ]
    assert len(opendp_lines) == 1
    assert "opendp[polars]==0.12.0" in opendp_lines[0].strip()
