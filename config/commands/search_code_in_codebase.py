#!/root/miniconda3/bin/python

# @yaml
# signature: search_method_in_codebase <code_str>
# docstring: Searches for the specified code_str in the codebase and prints the file path and line number about it.
# arguments:
#   code_str:
#       type: string
#       description: The snippet node to search for in the codebase.
#       required: true

import os
import ast
import sys


def search_code_in_codebase(code_str: str):
    current_working_directory = os.getcwd()
    snippet_tree = ast.parse(code_str).body

    found_any = False  # Flag to track if any matches are found

    for root, dirs, files in os.walk(current_working_directory):
        for file in files:
            if file.endswith('.py'):
                full_file_path = os.path.join(root, file)

                with open(full_file_path, 'r') as f:
                    file_content = f.read()

                tree = ast.parse(file_content)

                for node in ast.walk(tree):
                    if any(isinstance(node, type(snippet_node)) and ast.dump(node) == ast.dump(snippet_node)
                           for snippet_node in snippet_tree):
                        relative_file_path = os.path.relpath(full_file_path, current_working_directory)
                        print(f"{relative_file_path}, line {node.lineno}")
                        found_any = True

    if not found_any:
        print(f"Code snippet not found in the codebase.")


if __name__ == "__main__":
    search_code_in_codebase(sys.argv[1])
