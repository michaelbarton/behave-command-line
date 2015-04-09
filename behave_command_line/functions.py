import sys,os.path

import nose.tools                     as nt
import more_assertive_nose.assertions as asrt
import string                         as st

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
    contents = st.join([st.join(row, delimiter) for row in context.table], "\n")

    path = os.path.join(context.env.cwd,target)
    with open(path,'w') as f:
        f.write(contents)

@given(u'I gzip the file "{file_}"')
def step_impl(context, file_):
    import gzip
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
    import re

    arguments = st.join([st.join(row,' ') for row in context.table], ' ')
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
    nt.assert_in(output, s)

@then('the standard {stream} should contain')
def step_impl(context,stream):
    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise RuntimeError('Unknown stream "{}"'.format(stream))
    nt.assert_in(context.text.strip(), s)

@then('the standard {stream} should equal')
def step_impl(context,stream):
    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise RuntimeError('Unknown stream "{}"'.format(stream))
    asrt.assert_diff(context.text, s)

@then('The exit code should be {code}')
def step_impl(context,code):
    nt.assert_equal(context.output.returncode, int(code))

@then('the {thing} "{target}" should exist')
def step_impl(context, thing, target):
    nt.assert_in(target,context.output.files_created.keys(),
            "The {0} '{1}' does not exist.".format(thing, target))

@then('the {thing} "{target}" should not exist')
def step_impl(context, thing, target):
    nt.assert_not_in(target,context.output.files_created.keys(),
            "The {0} '{1}' does not exist.".format(thing, target))

@then('the files should exist')
def step_impl(context):
    for f in context.table:
        context.execute_steps(u'then the file "{}" should exist'.format(f['file']))

@then('the file "{target}" should exist with the contents')
def step_impl(context, target):
    nt.assert_in(target, context.output.files_created.keys(),
            "The file '{}' does not exist.".format(target))
    with open(context.output.files_created[target].full,'r') as f:
        asrt.assert_diff(context.text, f.read())

@then('the file "{target}" should contain "{contents}"')
def step_impt(context, target, contents):
    context.execute_steps(u'''
       Then the file "{}" should exist with the contents:
       """
       {}
       """'''.format(target, contents))

@then('the file "{target}" should include')
def step_impl(context,target):
    from re import search

    with open(context.output.files_created[target].full,'r') as f:
        contents = f.read()
        for row in context.table:
            regex = row['re_match'].strip()
            nt.assert_true(search(regex, contents),
                    "RE '{}' not found in: \n{}".format(regex, contents))

@then(u'the file "{target}" should should have the permissions "{permission}"')
def step_impl(context,target,permission):
    f = context.output.files_created[target].full
    asrt.assert_permission(f,permission)

@then('the standard {stream} should be empty')
def step_impl(context,stream):
    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise Error('Unknown stream "{}"').format(stream)
    asrt.assert_empty(s)

