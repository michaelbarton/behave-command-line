import pathlib
import tempfile
from unittest import mock

import pytest
import scripttest

from behave_command_line import functions
from behave import runner


@pytest.fixture
def directory() -> pathlib.Path:
    return pathlib.Path(tempfile.mkdtemp() + "/test")


@pytest.fixture
def context(directory: pathlib.Path) -> runner.Context:
    test_context = runner.Context(mock.MagicMock())
    test_context.env = scripttest.TestFileEnvironment(str(directory))
    return test_context


def test_create_the_file(directory: pathlib.Path, context: runner.Context) -> None:
    """Test creation of an empty file."""
    functions.create_the_file(context, "test_file")
    assert (directory / "test_file").exists()


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


def test_create_the_file_with() -> None:
    pass


def test_create_the_delimited_file_with() -> None:
    pass


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
