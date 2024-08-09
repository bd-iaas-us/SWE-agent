import pytest
import os
import shutil
from io import StringIO
import sys

from search_method_in_codebase import *

TEST_FOLDER_NAME = 'test_folder'


@pytest.fixture
def setup_test_files():
    current_working_directory = os.getcwd()
    test_dir = os.path.join(current_working_directory, TEST_FOLDER_NAME)
    os.makedirs(test_dir, exist_ok=True)

    file1_path = os.path.join(test_dir, 'file1.py')
    file2_path = os.path.join(test_dir, 'file2.py')
    sub_dir = os.path.join(test_dir, 'subdir')
    os.makedirs(sub_dir, exist_ok=True)
    file3_path = os.path.join(sub_dir, 'file3.py')

    with open(file1_path, 'w') as f1:
        f1.write("""def method_1():
    pass

def method_2():
    pass
""")

    with open(file2_path, 'w') as f2:
        f2.write("""def method_3():
    pass
""")

    with open(file3_path, 'w') as f3:
        f3.write("""def method_1():
    pass
""")

    yield file1_path, file2_path, file3_path

    # Clean up after test
    shutil.rmtree(test_dir)


def test_search_method_in_codebase_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_codebase('method_1')

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'test_folder/file1.py, line 1' in output
        assert 'test_folder/subdir/file3.py, line 1' in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_method_in_codebase_not_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_codebase('non_existent_method')

        # Capture the output
        output = sys.stdout.getvalue()

        assert "Method 'non_existent_method' not found in the codebase." in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout

