import subprocess
from pathlib import Path


# TODO: Need to handle errors in the script call.
def execute(
        command: str | list[str],
        path: str | Path,
):
    output = subprocess.run(
        command, cwd=path, shell=False, text=True, capture_output=True,
    )

    return output.stdout.strip()
