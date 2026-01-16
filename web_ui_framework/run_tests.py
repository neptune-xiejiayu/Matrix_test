import sys
import pytest


if __name__ == "__main__":
    args = ["-q"] + sys.argv[1:]
    sys.exit(pytest.main(args))
