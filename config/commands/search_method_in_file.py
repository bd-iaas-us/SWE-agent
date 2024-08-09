#!/root/miniconda3/bin/python

# @yaml
# signature: search_method_in_file <method_name> <file_path>
# docstring: Search for the specified method_name in the given file and prints the file path and line number about it.
# arguments:
#   method_name:
#       type: string
#       description: The name of the method to search for in the file.
#       required: true
#   file_path:
#       type: string
#       description: The relative path to the file to search for.
#       required: true

import ast
import os
import sys


def search_method_in_file(method_name: str, file_path: str):
    current_working_directory = os.getcwd()
    full_file_path = os.path.join(current_working_directory, file_path)

    # Ensure the file exists
    if not os.path.isfile(full_file_path):
        raise FileNotFoundError(f"The file '{full_file_path}' does not exist.")

    with open(full_file_path, 'r') as file:
        file_content = file.read()

    tree = ast.parse(file_content)

    found_any = False  # Flag to track if any matches are found

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            relative_file_path = os.path.relpath(full_file_path, current_working_directory)
            print(f"{relative_file_path}, line {node.lineno}")
            found_any = True

    if not found_any:
        print(f"Method_name {method_name} not found in the file.")


if __name__ == "__main__":
    search_method_in_file(sys.argv[1], sys.argv[2])
