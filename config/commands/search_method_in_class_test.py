import pytest
import os
import shutil
from io import StringIO
import sys

from search_method_in_class import *

TEST_FOLDER_NAME = 'test_folder'


@pytest.fixture
def setup_test_files():
    current_working_directory = os.getcwd()
    test_dir = os.path.join(current_working_directory, TEST_FOLDER_NAME)
    os.makedirs(test_dir, exist_ok=True)

    temp_file_path = os.path.join(test_dir, 'test_file_1.py')
    temp_file_path_2 = os.path.join(test_dir, 'test_file_2.py')

    with open(temp_file_path, 'w') as f:
        f.write("""class TargetClass:
    def method_1(self):
        pass

    def method_2(self):
        pass
""")

    with open(temp_file_path_2, 'w') as f:
        f.write("""class AnotherClass:
    def method_1(self):
        pass
""")

    yield temp_file_path, temp_file_path_2

    # Clean up after test
    shutil.rmtree(test_dir)


def test_search_method_in_class_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_class('method_1', 'TargetClass')

        # Capture the output
        output = sys.stdout.getvalue()

        assert 'test_folder/test_file_1.py, line 2' in output
    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_method_in_class_not_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_class('non_existent_method', 'TargetClass')

        # Capture the output
        output = sys.stdout.getvalue()

        assert "Method 'non_existent_method' in class 'TargetClass' not found in any file." in output
    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_search_class_not_found(setup_test_files):
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_class('method_2', 'NonExistentClass')

        # Capture the output
        output = sys.stdout.getvalue()

        assert "Method 'method_2' in class 'NonExistentClass' not found in any file." in output
    finally:
        # Restore stdout
        sys.stdout = old_stdout


def test_file_not_found():
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        search_method_in_class('method_3', 'TargetClass')

        # Capture the output
        output = sys.stdout.getvalue()

        assert "Method 'method_3' in class 'TargetClass' not found in any file." in output

    finally:
        # Restore stdout
        sys.stdout = old_stdout
