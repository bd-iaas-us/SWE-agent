import pytest
import os
import shutil
from io import StringIO
import sys

from search_code_in_codebase import *

TEST_FOLDER_NAME = 'test_folder'


@pytest.fixture
def setup_test_files():
    current_working_directory = os.getcwd()
    test_dir = os.path.join(current_working_directory, TEST_FOLDER_NAME)
    os.makedirs(test_dir, exist_ok=True)

    file1_path = os.path.join(test_dir, 'file1.py')
    file2_path = os.path.join(test_dir, 'file2.py')
    sub_dir = os.path.join(test_dir, 'dir')
    os.makedirs(sub_dir, exist_ok=True)
    file3_path = os.path.join(sub_dir, 'file3.py')

    with open(file1_path, 'w') as f1:
        f1.write("""def method_1():
    print("sample code 1")

def method_2():
    pass
""")

    with open(file2_path, 'w') as f2:
        f2.write("""class Class_2:
    def method_2(self):
        print("sample code 2")
""")

    with open(file3_path, 'w') as f3:
        f3.write("""def method_3():
    print("sample code 1")
""")

    yield file1_path, file2_path, file3_path

    # Clean up after test
    shutil.rmtree(test_dir)


def test_search_code_in_codebase_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        code_snippet = """print("sample code 1")"""
        search_code_in_codebase(code_snippet)

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'test_folder/file1.py, line 2' in output
        assert 'test_folder/dir/file3.py, line 2' in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_nested_code_in_codebase_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        code_snippet = """def method_2(self):
        print("sample code 2")"""
        search_code_in_codebase(code_snippet)

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'test_folder/file2.py, line 2' in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_code_in_codebase_not_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        code_snippet = """print("Code snippet not found")"""

        search_code_in_codebase(code_snippet)

        # Capture the output
        output = sys.stdout.getvalue()

        assert "Code snippet not found in the codebase." in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout
