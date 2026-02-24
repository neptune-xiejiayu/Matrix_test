import sys
import os
import pytest


if __name__ == "__main__":
    # Ensure repository root is on sys.path so tests can import the package
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(repo_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    args = ["-q"] + sys.argv[1:]
    sys.exit(pytest.main(args))
