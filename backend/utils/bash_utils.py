import json
import subprocess


def bash(command: str, to_json: bool = False) -> str | dict | None:
    response = None
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        response = result.stdout.strip()
        if result.stderr:
            print(f"Error: {result.stderr.strip()}")
    except Exception as ex:
        print(f"Exception: {ex}")
    if response and to_json:
        return json.loads(response)
    return response
