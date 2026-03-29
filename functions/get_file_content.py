import os

from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_directory = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        contents = ""
        with open(target_file, "r") as f:
            contents += f.read(MAX_CHARS)
            if f.read(1):
                contents += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return contents
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file",
            )
        },
        required=["file_path"],
    ),
)
