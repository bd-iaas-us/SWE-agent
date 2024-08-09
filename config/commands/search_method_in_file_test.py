import pytest
import os
import shutil
from io import StringIO
import sys

from search_method_in_file import *

TEST_FOLDER_NAME = 'test_folder'


@pytest.fixture
def setup_test_files():
    current_working_directory = os.getcwd()
    test_dir = os.path.join(current_working_directory, TEST_FOLDER_NAME)
    os.makedirs(test_dir, exist_ok=True)
    temp_file_path = os.path.join(test_dir, 'test_file.py')

    with open(temp_file_path, 'w') as f:
        f.write("""def method_1():
    pass

def method_2():
    pass
""")

    yield temp_file_path

    # Clean up after test
    shutil.rmtree(test_dir)


def test_search_target_method_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_file('method_1', 'test_folder/test_file.py')

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'test_folder/test_file.py, line 1' in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_another_method_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_file('method_2', 'test_folder/test_file.py')

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'test_folder/test_file.py, line 4' in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_method_not_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_file('non_existent_method', 'test_folder/test_file.py')

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'Method_name non_existent_method not found in the file.' in output
    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_file_not_found():
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        with pytest.raises(FileNotFoundError):
            search_method_in_file('method_1', 'test_folder/non_existent_file.py')

    finally:
        # Restore stdout
        sys.stdout = old_stdout
