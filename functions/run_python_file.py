import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))

        valid_path = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command, cwd=abs_path, capture_output=True, text=True, timeout=30
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"
