#!/root/miniconda3/bin/python

# @yaml
# signature: search_code_in_file <code_str> <file_path>
# docstring: Searches for the specified code_str in the codebase and prints the file path and line number about it.
# arguments:
#   code_str:
#       type: string
#       description: The snippet node to search for in the codebase.
#       required: true
#   file_path:
#       type: string
#       description: The relative path to the file to search for.
#       required: true

import ast
import os
import sys


def search_code_in_file(code_str: str, file_path: str):
    current_working_directory = os.getcwd()
    full_file_path = os.path.join(current_working_directory, file_path)

    # Ensure the file exists
    if not os.path.isfile(full_file_path):
        raise FileNotFoundError(f"The file '{full_file_path}' does not exist.")

    with open(full_file_path, 'r') as file:
        file_content = file.read()

    snippet_tree = ast.parse(code_str).body
    file_tree = ast.parse(file_content)

    found_any = False  # Flag to track if any matches are found

    for node in ast.walk(file_tree):
        if any(isinstance(node, type(snippet_node)) and ast.dump(node) == ast.dump(snippet_node)
               for snippet_node in snippet_tree):
            relative_file_path = os.path.relpath(full_file_path, current_working_directory)
            print(f"{relative_file_path}, line {node.lineno}")
            found_any = True

    if not found_any:
        print(f"Code snippet not found in the file.")


if __name__ == "__main__":
    search_code_in_file(sys.argv[1], sys.argv[2])
