import argparse
import os
import subprocess
import sys

REQUIRED_TOOLS = [
    "autopep8",
    "black",
    "isort",
    "bandit",
    "codespell",
    "flake8",
    "pylint",
]

def check_and_install_tools():
    """Check if required tools are installed and install them if not."""
    missing_tools = [tool for tool in REQUIRED_TOOLS if not is_tool_installed(tool)]
    if missing_tools:
        print(f"Missing tools detected: {', '.join(missing_tools)}")
        print("Installing missing tools...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_tools])
    else:
        print("All required tools are installed.")

def is_tool_installed(tool_name):
    """Check if a tool is installed."""
    try:
        subprocess.check_output([tool_name, "--version"], stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_tool(command, description):
    """Run a formatting tool and handle errors."""
    print(f"Running {description}...")
    try:
        subprocess.check_call(command, shell=True)
        print(f"{description} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {description}: {e}")
    except Exception as e:
        print(f"Unexpected error while running {description}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Run code quality tools on a specified relative path from the repository's main directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        default="psychopy_bids",
        help="Relative path to run tools on (default: psychopy_bids). Use '.' for the whole repository.",
    )
    args = parser.parse_args()
    target_path = args.path

    # Change the working directory to the parent directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    os.chdir(parent_dir)
    print(f"Changed working directory to: {parent_dir}")

    # Check and install required tools
    check_and_install_tools()

    # Run tools on the specified path
    run_tool(f"isort {target_path}", "isort")
    run_tool(f"black {target_path}", "black")
    run_tool(
        f"autopep8 --in-place --recursive --max-line-length 99 {target_path}",
        "autopep8",
    )
    run_tool(f"bandit -q -r {target_path}", "bandit")
    run_tool(f'codespell --ignore-words-list="assertIn" {target_path}', "codespell")
    run_tool(f"flake8 --ignore=E501,W503,F841 {target_path}", "flake8")

    # Run pylint
    run_tool("pip install -q numpy pandas requests", "Install imports")
    run_tool("pip install -q psychopy --no-deps", "Install psychopy --no-deps")
    run_tool("pip install -q psychopy-bids --no-deps", "Install psychopy-bids -no-deps")

    if target_path != "psychopy_bids":
        run_tool(f"pylint {target_path}", "pylint")
    else:
        run_tool(
            "pylint --method-naming-style=camelCase -d C0123,C0301,C0301,C0302,R0902,R0912,R0913,R0914,R0915,R0917,R1702,W0511 psychopy_bids/bids/*.py",
            "pylint (bids)",
        )
        run_tool(
            "pylint -d C0103,C0301,R0912,R0913,R0914,R0915,R0917,W0212,W0511,W0612 psychopy_bids/bids_event/*.py",
            "pylint (bids_event)",
        )
        run_tool(
            "pylint -d C0103,C0301,R0913,R0915,R0917,W0511 psychopy_bids/bids_settings/*.py",
            "pylint (bids_settings)",
        )


if __name__ == "__main__":
    main()
