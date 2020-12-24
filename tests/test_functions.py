import pathlib
import tempfile
import textwrap
from unittest import mock

import pytest
import scripttest

from behave_command_line import functions
from behave import runner


@pytest.fixture
def directory() -> pathlib.Path:
    return pathlib.Path(tempfile.mkdtemp() + "/test")


@pytest.fixture
def test_file(directory: pathlib.Path) -> pathlib.Path:
    return directory / "test_file"


@pytest.fixture
def context(directory: pathlib.Path) -> runner.Context:
    test_context = runner.Context(mock.MagicMock())
    test_context.env = scripttest.TestFileEnvironment(str(directory))
    return test_context


def test_create_the_file(test_file: pathlib.Path, context: runner.Context) -> None:
    """Test creation of an empty file."""
    functions.create_the_file(context, test_file.name)
    assert test_file.exists()


@pytest.mark.parametrize("path_type", ("file", "directory"))
def test_delete_the_path(path_type: str, directory: pathlib.Path, context: runner.Context) -> None:
    """Test a file system path can be deleted."""
    file_path = directory / "test_file"
    if path_type == "file":
        file_path.touch()
    else:
        file_path.mkdir()
    functions.delete_filesystem_path(context, path_type, str(file_path.absolute()))
    assert not file_path.exists()


def test_create_the_file_with(test_file: pathlib.Path, context: runner.Context) -> None:
    """Test a file can be created with contents"""
    context.text = "Some text"
    functions.create_the_file_with(context, test_file.name)
    assert test_file.read_text() == "Some text"


@pytest.mark.parametrize("delimiter", [",", "|"])
def test_create_the_delimited_file_with(delimiter: str, test_file: pathlib.Path, context: runner.Context) -> None:
    context.table = [{"col_1": 1, "col_2": 2}, {"col_1": 3, "col_2": 4}]
    functions.create_the_delimited_file_with(context, delimiter, test_file.name)
    assert test_file.read_text().strip() == textwrap.dedent(f"""\
        col_1{delimiter}col_2
        1{delimiter}2
        3{delimiter}4
    """).strip()


def test_gzip_the_file() -> None:
    pass


def test_create_the_directory() -> None:
    pass


def test_run_the_command_with_args() -> None:
    pass


def test_run_the_command() -> None:
    pass


def test_the_stream_should_contain() -> None:
    pass


def test_the_stream_should_contain_text() -> None:
    pass


def test_the_stream_should_equal() -> None:
    pass


def test_the_exit_code_should_be() -> None:
    pass


def test_the_io_type_was_created() -> None:
    pass


def test_the_io_type_should_not_exist() -> None:
    pass


def test_the_files_should_exist() -> None:
    pass


def test_the_file_should_exist_with() -> None:
    pass


def test_the_file_should_contain() -> None:
    pass


def test_the_file_should_include() -> None:
    pass


def test_the_file_should_have_permissions() -> None:
    pass


def test_the_stream_should_be_empty() -> None:
    pass
