#!/root/miniconda3/bin/python

# @yaml
# signature: search_class <class_name>
# docstring: Searches for the specified class_name in the codebase and prints the file path and line number about it.
# arguments:
#   class_name:
#       type: string
#       description: The name of the class to search for in the codebase.
#       required: true


import ast
import os
import sys


class ClassVisitor(ast.NodeVisitor):
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.matches = []

    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            self.matches.append(node)
        self.generic_visit(node)


def search_class(class_name: str):
    found_any = False  # Flag to track if any matches are found
    current_working_directory = os.getcwd()
    for root, dirs, files in os.walk(current_working_directory):
        for file in files:
            if file.endswith(".py"):
                file_full_path = os.path.join(root, file)
                with open(file_full_path, 'r') as f:
                    file_content = f.read()

                tree = ast.parse(file_content)
                visitor = ClassVisitor(class_name)
                visitor.visit(tree)
                for match in visitor.matches:
                    relative_path = os.path.relpath(file_full_path, current_working_directory)
                    print(f"{relative_path}, line {match.lineno}")
                    found_any = True

    if not found_any:
        print(f"Class {class_name} not found in the project.")


if __name__ == "__main__":
    search_class(sys.argv[1])

