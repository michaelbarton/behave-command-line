import gzip
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
    """Test can create a tab delimited file as step."""
    context.table = [{"col_1": 1, "col_2": 2}, {"col_1": 3, "col_2": 4}]
    functions.create_the_delimited_file_with(context, delimiter, test_file.name)
    assert test_file.read_text().strip() == textwrap.dedent(f"""
        col_1{delimiter}col_2
        1{delimiter}2
        3{delimiter}4
    """).strip()


def test_gzip_the_file(test_file: pathlib.Path, context: runner.Context) -> None:
    """Test can create a gzipped file."""
    example_text = "some text\nfor testing"
    test_file.write_text(example_text)
    functions.gzip_the_file(context, str(test_file))

    with gzip.open(str(test_file) + ".gz", 'rb') as gzip_in:
        assert gzip_in.read().decode("utf-8") == example_text


def test_create_the_directory(directory: pathlib.Path, context: runner.Context) -> None:
    """Test a directory can be created."""
    new_dir = directory / "test_dir"
    functions.create_the_directory(context, str(new_dir))
    assert new_dir.exists()
    assert new_dir.is_dir()


def test_run_the_command_with_args(context: runner.Context) -> None:
    """Test command can be run with arguments in a context table."""
    context.table = [{"arg": "-l"}, {"arg": "-r"}, {"arg": "/"}]
    functions.run_the_command_with_args(context, "ls")
    assert not context.output.stderr
    assert context.output.stdout
    assert context.output.returncode == 0


def test_run_the_command(context: runner.Context) -> None:
    """Test can run command as a string."""
    functions.run_the_command(context, "ls -lt /")
    assert not context.output.stderr
    assert context.output.stdout
    assert context.output.returncode == 0


@pytest.mark.parametrize("should_fail,stream", [
    (True, "stderr"),
    (False, "stderr"),
    (True, "stdout"),
    (False, "stdout"),
])
def test_the_stream_should_contain(should_fail: bool, stream: str, context: runner.Context) -> None:
    test_value = "value"
    context.output = mock.MagicMock()
    if should_fail:
        setattr(context.output, stream, "failing")
    else:
        setattr(context.output, stream, test_file)

    try:
        functions.the_stream_should_contain(context, stream.replace("std", ""), test_value)
    except AssertionError:
        if should_fail:
            return
        pytest.fail("Should not fail when value is in string.")

    if should_fail:
        pytest.fail("Should fail when value is not in string.")


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
