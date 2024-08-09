import pytest
import os
import shutil
from io import StringIO
import sys

from search_code_in_file import *


TEST_FOLDER_NAME = 'test_folder'

@pytest.fixture()
def setup_test_files():
    # Setup: Create a test directory and test file
    current_working_directory = os.getcwd()
    test_dir = os.path.join(current_working_directory, TEST_FOLDER_NAME)
    os.makedirs(test_dir, exist_ok=True)

    file1_path = os.path.join(test_dir, "test_file_1.py")
    with open(file1_path, 'w') as f:
        f.write('''def method_1():
    print("sample code 1")
    print("sample code 3")

def method_2():
    pass
''')

    file2_path = os.path.join(test_dir, 'test_file_2.py')
    with open(file2_path, 'w') as f2:
        f2.write("""class Class_2:
        def method_2(self):
            print("sample code 2")
    """)
    yield file1_path, file2_path

    # Clean up after test
    shutil.rmtree(test_dir)


def test_search_code_in_file_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        code_snippet = """print("sample code 1")"""
        search_code_in_file(code_snippet, "test_folder/test_file_1.py")

        # Capture the output
        output = sys.stdout.getvalue()

        assert "test_folder/test_file_1.py, line 2" in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_nested_code_in_file_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        code_snippet = """def method_2(self):
                print("sample code 2")"""
        search_code_in_file(code_snippet, "test_folder/test_file_2.py")


        # Capture the output
        output = sys.stdout.getvalue()

        assert "test_folder/test_file_2.py, line 2" in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_code_in_file_not_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        code_snippet = """print("Code snippet not found")"""

        search_code_in_file(code_snippet, "test_folder/test_file_2.py")

        # Capture the output
        output = sys.stdout.getvalue()

        assert "Code snippet not found in the file." in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_file_not_found():
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        with pytest.raises(FileNotFoundError):
            search_code_in_file("""print("sample code 1")""", 'test_folder/non_existent_file.py')

    finally:
        # Restore stdout
        sys.stdout = old_stdout

