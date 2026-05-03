import sys
import os

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
STRATEGIES_DIR = os.path.dirname(TESTS_DIR)

sys.path.insert(0, TESTS_DIR)
sys.path.insert(0, STRATEGIES_DIR)

from mock_qc import install_mock
install_mock()


def pytest_addoption(parser):
    parser.addoption(
        "--update-baseline", action="store_true", default=False,
        help="Accept fresh QC results as the new baseline",
    )
