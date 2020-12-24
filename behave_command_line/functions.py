"""Behave step matchers for working with the file system and command line tools."""

import csv
import gzip
import os.path
import pathlib
import re

import behave
from behave import runner


def get_stream(context: runner.Context, stream_name: str) -> str:
    """Get a stream type from a scripttest context.

    Args:
        context: Behave runner context.
        stream_name: Name of which stream to fetch.

    Returns:
        The contents of that stream.

    Raises:
        ValueError: If the given stream name was not out or error.

    """
    if stream_name == "out":
        return str(context.output.stdout)
    if stream_name == "error":
        return str(context.output.stderr)
    raise ValueError('Unknown stream "{}"'.format(stream_name))


@behave.given('I create the file "{target}"')
def create_the_file(context: runner.Context, target: str) -> None:
    """Create a file in the context.

    Args:
        context: Behave runner context
        target: Name of the file to create.
    """
    context.env.run("touch", target)


@behave.given('I delete the {io_type} "{target}"')
def delete_filesystem_path(context: runner.Context, io_type: str, target: str) -> None:
    """Delete a given file system path.

    Args:
        context: Behave runner context
        io_type: Unused string describing the file system object type
        target: File system object name to remove.

    """
    _ = io_type
    if not pathlib.Path(target).exists():
        raise RuntimeError(f"Cannot delete `{target}`, does not exist.")
    context.env.run("rm", "-r", target)


@behave.given('I create the file "{target}" with the contents')
def create_the_file_with(context: runner.Context, target: str) -> None:
    """Create the file with the given contents.

    Args:
        context: Behave runner context with file contents.
        target: Name of the file to create.

    """
    path = os.path.join(context.env.cwd, target)
    with open(path, "w") as target_file:
        target_file.write(context.text)


@behave.given(u'I create a "{delimiter}" delimited file "{target}" with the contents')
def create_the_delimited_file_with(context: runner.Context, delimiter: str, target: str) -> None:
    """Create a delimited file with contents.

    Args:
        context: Behave runner context with file contents.
        delimiter: Delimiter to use.
        target: Name of file to create.

    """
    path = os.path.join(context.env.cwd, target)
    with open(path, "w") as target_file:
        writer = csv.DictWriter(target_file, fieldnames=context.table[0].keys(), delimiter=delimiter)
        writer.writeheader()
        for row in context.table:
            writer.writerow(row)


@behave.given(u'I gzip the file "{target}"')
def gzip_the_file(context: runner.Context, target: str) -> None:
    """Gzip a file

    Args:
        context: Behave runner context
        target: Name of the file to gzip.

    """
    path = os.path.join(context.env.cwd, target)
    with open(path, "rb") as f_in:
        with gzip.open(path + ".gz", "wb") as f_out:
            f_out.writelines(f_in)


@behave.given('I create the directory "{target}"')
def create_the_directory(context: runner.Context, target: str) -> None:
    """Create a directory.

    Args:
        context: Behave runner context.
        target: Name of the directory to create.

    """
    path = os.path.join(context.env.cwd, target)
    os.makedirs(path)


@behave.when('I run the command "{command}" with the arguments')
def run_the_command_with_args(context: runner.Context, command: str) -> None:
    """Run a command with the arguments given in the context table.

    Args:
        context: Behave context with a table of arguments.
        command: Script or binary to run.

    """

    # TODO: Use library to escape bad characters such as semi colons
    arguments = " ".join([" ".join(row) for row in context.table])
    arguments = re.sub(r"\s+", " ", arguments.strip())

    context.output = context.env.run(
        command, *arguments.split(" "), expect_error=True, expect_stderr=True
    )


@behave.when('I run the command "{command}"')
def run_the_command(context: runner.Context, command: str) -> None:
    """Run a command and arguments.

    Args:
        context: Behave runner context.
        command: Command and arguments to run.

    """
    context.output = context.env.run(command, expect_error=True, expect_stderr=True)


@behave.when('the standard {stream} should contain "{expected_contents}"')
def the_stream_should_contain(context: runner.Context, stream: str, expected_contents: str) -> None:
    """Ensure the given command stream output stream contains a string.

    Args:
        context: Behave runner context.
        stream: Name of the stream to check.
        expected_contents: Contents which should be in the stream.

    """
    assert expected_contents in get_stream(context, stream)


@behave.when("the standard {stream} should contain")
def the_stream_should_contain_text(context: runner.Context, stream: str) -> None:
    """Ensure a given command stream contains a text block.

    Args:
        context: Behave runner context with a text block to check in the stream.
        stream: Name of the stream to check for.

    """
    assert context.text.strip() in get_stream(context, stream)


@behave.when("the standard {stream} should equal")
def the_stream_should_equal(context: runner.Context, stream: str) -> None:
    """Check an output stream is equal to a text block.

    Args:
        context: Behave runner context with a text block.
        stream: Name of the stream to check for.

    """
    assert get_stream(context, stream) == context.text


@behave.when("The exit code should be {code}")
def the_exit_code_should_be(context: runner.Context, code: str) -> None:
    """Check expected output code for a command.

    Args:
        context: Behave runner context.
        code: Expected exit code.

    """
    assert context.output.returncode == int(code)


@behave.when('the {io_type} "{target}" should exist')
def the_io_type_was_created(context: runner.Context, io_type: str, target: str) -> None:
    """Check an io type exists

    Args:
        context: Behave runner context.
        io_type: Type of io object that should have been created.
        target: Nmae of io type that should have been created.

    """
    assert target in context.output.files_created.keys(), "The {0} '{1}' was not created.".format(
        io_type, target
    )


@behave.when('the {io_type} "{target}" should not exist')
def the_io_type_should_not_exist(context: runner.Context, io_type: str, target: str) -> None:
    """Check an io type was not created.

    Args:
        context: Behave runner context.
        io_type: Name of IO type that should have not be created.
        target: Name of target that should have been created.

    """
    assert (
        target not in context.output.files_created.keys()
    ), "The {0} '{1}' does not existring.".format(io_type, target)


@behave.when("the files should exist")
def the_files_should_exist(context: runner.Context) -> None:
    """Check a list of files that should have been created.

    Args:
        context: Behave runner context with a list of files.

    """
    for target_file in context.table:
        context.execute_steps(u'then the file "{}" should exist'.format(target_file["file"]))


@behave.when('the file "{target}" should exist with the contents')
def the_file_should_exist_with(context: runner.Context, target: str) -> None:
    """Check a file exists with a text block.

    Args:
        context: Behave runner context with a text block.
        target: Name of the file to check.

    """
    assert (
        target in context.output.files_created.keys()
    ), "The file '{}' does not existring.".format(target)
    with open(context.output.files_created[target].full, "r") as target_file:
        assert target_file.read() == context.text


@behave.when('the file "{target}" should contain "{contents}"')
def the_file_should_contain(context: runner.Context, target: str, contents: str) -> None:
    """Check a file contains a given string.

    Args:
        context: Behave runner context.
        target: Name of file to check.
        contents: Expected contents of file.

    """
    context.execute_steps(
        """
       Then the file "{}" should exist with the contents:
       '''
       {}
       '''
        """.format(
            target, contents
        )
    )


@behave.when('the file "{target}" should include')
def the_file_should_include(context: runner.Context, target: str) -> None:
    """Check a file contains a given text block.

    Args:
        context: Behave runner context with text block.
        target: Name of file to check.

    """

    with open(context.output.files_created[target].full) as target_file:
        contents = target_file.read()
        for row in context.table:
            regex = row["re_match"].strip()
            assert re.search(regex, contents), "RE '{}' not found in: \n{}".format(regex, contents)


@behave.when(u'the file "{target}" should should have the permissions "{permission}"')
def the_file_should_have_permissions(context: runner.Context, target: str, permission: str) -> None:
    """Check file has expected permissions.

    Args:
        context: Behave runner context.
        target: Name of file to check.
        permission: Expected set of permissions.

    """
    target_file = context.output.files_created[target].full
    assert os.stat(target_file).st_mode == permission


@behave.when("the standard {stream} should be empty")
def the_stream_should_be_empty(context: runner.Context, stream: str) -> None:
    """Check a command line output stream is empty.

    Args:
        context: Behave context.
        stream: Name of string to check.

    """
    stream_contents = get_stream(context, stream)
    assert not stream_contents, "Expected the std{} to be empty but was:\n{}".format(
        stream, stream_contents
    )
