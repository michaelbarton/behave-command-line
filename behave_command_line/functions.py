import gzip
import os.path
import re
import string

from behave import *

@given('I create the file "{target}"')
def step_impl(context,target):
    context.env.run('touch', target)

@given('I delete the {_} "{target}"')
def step_impl(context, _, target):
    context.env.run('rm', '-r', target)

@given('I create the file "{target}" with the contents')
def step_impl(context,target):
    path = os.path.join(context.env.cwd,target)
    with open(path,'w') as f:
        f.write(context.text)

@given(u'I create a "{delimiter}" delimited file "{target}" with the contents')
def step_impl(context, delimiter, target):
    contents = string.join([string.join(row, delimiter) for row in context.table], "\n")

    path = os.path.join(context.env.cwd,target)
    with open(path,'w') as f:
        f.write(contents)

@given(u'I gzip the file "{file_}"')
def step_impl(context, file_):
    path = os.path.join(context.env.cwd,file_)
    with open(path, 'rb') as f_in:
        with gzip.open(path + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)

@given('I create the directory "{target}"')
def step_impl(context,target):
    path = os.path.join(context.env.cwd,target)
    os.makedirs(path)

@when('I run the command "{command}" with the arguments')
def step_impl(context, command):

    arguments = string.join([string.join(row,' ') for row in context.table], ' ')
    arguments = re.sub(r'\s+', ' ', arguments.strip())

    context.output = context.env.run(command, *arguments.split(' '),
        expect_error  = True,
        expect_stderr = True)

@when('I run the command "{command}"')
def step_impl(context, command):
    context.output = context.env.run(command,
        expect_error  = True,
        expect_stderr = True)

@then('the standard {stream} should contain "{output}"')
def step_impl(context, stream, output):
    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise RuntimeError('Unknown stream "{}"'.format(stream))
    assert s in output

@then('the standard {stream} should contain')
def step_impl(context,stream):
    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise RuntimeError('Unknown stream "{}"'.format(stream))
    assert s in context.text.strip()

@then('the standard {stream} should equal')
def step_impl(context,stream):
    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise RuntimeError('Unknown stream "{}"'.format(stream))
    assert s == context.text

@then('The exit code should be {code}')
def step_impl(context,code):
    assert context.output.returncode == int(code)

@then('the {thing} "{target}" should exist')
def step_impl(context, thing, target):
    assert target in context.output.files_created.keys(), "The {0} '{1}' does not existring.".format(thing, target)

@then('the {thing} "{target}" should not exist')
def step_impl(context, thing, target):
    assert target not in context.output.files_created.keys(), "The {0} '{1}' does not existring.".format(thing, target)

@then('the files should exist')
def step_impl(context):
    for f in context.table:
        context.execute_steps(u'then the file "{}" should exist'.format(f['file']))

@then('the file "{target}" should exist with the contents')
def step_impl(context, target):
    assert target in context.output.files_created.keys(), "The file '{}' does not existring.".format(target)
    with open(context.output.files_created[target].full,'r') as f:
        assert f.read() == context.text

@then('the file "{target}" should contain "{contents}"')
def step_impt(context, target, contents):
    context.execute_steps(u'''
       Then the file "{}" should exist with the contents:
       """
       {}
       """'''.format(target, contents))

@then('the file "{target}" should include')
def step_impl(context,target):

    with open(context.output.files_created[target].full,'r') as f:
        contents = f.read()
        for row in context.table:
            regex = row['re_match'].strip()
            assert re.search(regex, contents), "RE '{}' not found in: \n{}".format(regex, contents)

@then(u'the file "{target}" should should have the permissions "{permission}"')
def step_impl(context,target,permission):
    f = context.output.files_created[target].full
    assert os.stat(f).st_mode == permission

@then('the standard {stream} should be empty')
def step_impl(context,stream):
    if stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise ValueError('Unknown stream "{}"'.format(stream))
    assert not s

