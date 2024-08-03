import os
import pytest
import shutil
from io import StringIO
from contextlib import redirect_stdout

from search_class import *


TEST_FILE_NAME_1 = "test_file1.py"
TEST_FILE_NAME_2 = "test_file2.py"
TEST_FILE_NAME_3 = "test_file3.py"
TEST_FOLDER_NAME = "test_project"


@pytest.fixture
def setup_test_files():
    current_working_directory = os.getcwd()
    test_dir = os.path.join(current_working_directory, TEST_FOLDER_NAME)
    os.makedirs(test_dir, exist_ok=True)

    file1 = os.path.join(test_dir, TEST_FILE_NAME_1)
    with open(file1, 'w') as f:
        f.write("""class MyClass:
    def method1(self):
        pass
""")

    file2 = os.path.join(test_dir, TEST_FILE_NAME_2)
    with open(file2, 'w') as f:
        f.write("""class MyClass:
    def method2(self):
        pass
""")

    file3 = os.path.join(test_dir, TEST_FILE_NAME_3)
    with open(file3, 'w') as f:
        f.write("""class AnotherClass:
    def method1(self):
        pass
""")

    yield test_dir

    cleanup_test_files(test_dir)


def cleanup_test_files(test_dir):
    """Remove the test directory and its contents."""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_search_class_found(setup_test_files):
    test_dir = setup_test_files

    class_name = "MyClass"
    expected_output = [
        os.path.join(TEST_FOLDER_NAME, TEST_FILE_NAME_1) + ", line 1",  # test_project/test_file1.py
        os.path.join(TEST_FOLDER_NAME, TEST_FILE_NAME_2) + ", line 1",
    ]

    # Capture the output
    f = StringIO()
    with redirect_stdout(f):
        search_class(class_name)

    output = f.getvalue().strip().split('\n')

    for eo in expected_output:
        assert eo in output

    assert f"Class {class_name} not found in the project." not in output


def test_search_class_not_found(setup_test_files):
    test_dir = setup_test_files
    os.chdir(test_dir)

    class_name = "NonExistentClass"

    # Capture the output
    f = StringIO()
    with redirect_stdout(f):
        search_class(class_name)

    output = f.getvalue().strip()

    assert f"Class {class_name} not found in the project." in output


