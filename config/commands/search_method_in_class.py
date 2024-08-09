#!/root/miniconda3/bin/python

# @yaml
# signature: search_method_in_class <method_name> <class_name>
# docstring: Search for the specified method_name in the given class and prints the file path and line number about it.
# arguments:
#   method_name:
#       type: string
#       description: The name of the method to search for in the class.
#       required: true
#   class_name:
#       type: string
#       description: The name of the class to search for.
#       required: true


import os
import ast
import sys


def search_method_in_class(method_name: str, class_name: str):
    current_working_directory = os.getcwd()

    found_any = False  # Flag to track if any matches are found

    for root, dirs, files in os.walk(current_working_directory):
        for file in files:
            if file.endswith('.py'):
                full_file_path = os.path.join(root, file)

                with open(full_file_path, 'r') as f:
                    file_content = f.read()

                tree = ast.parse(file_content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef) and node.name == class_name:
                        for body_item in node.body:
                            if isinstance(body_item, ast.FunctionDef) and body_item.name == method_name:
                                relative_file_path = os.path.relpath(full_file_path, current_working_directory)
                                print(f"{relative_file_path}, line {body_item.lineno}")
                                found_any = True

    if not found_any:
        print(f"Method '{method_name}' in class '{class_name}' not found in any file.")


if __name__ == "__main__":
    search_method_in_class(sys.argv[1], sys.argv[2])
