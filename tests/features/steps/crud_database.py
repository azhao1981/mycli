# -*- coding: utf-8 -*-
"""
Steps for behavioral style tests are defined in this module.
Each step is defined by the string decorating it.
This string is used to call the step in "*.feature" file.
"""
from __future__ import unicode_literals

import pexpect

import wrappers
from behave import when, then


@when('we create database')
def step_db_create(context):
    """
    Send create database.
    """
    context.cli.sendline('create database {0};'.format(
        context.conf['dbname_tmp']))

    context.response = {
        'database_name': context.conf['dbname_tmp']
    }


@when('we drop database')
def step_db_drop(context):
    """
    Send drop database.
    """
    context.cli.sendline('drop database {0};'.format(
        context.conf['dbname_tmp']))

    wrappers.expect_exact(context, 'You\'re about to run a destructive command.\r\nDo you want to proceed? (y/n):', timeout=2)
    context.cli.sendline('y')

@when('we connect to test database')
def step_db_connect_test(context):
    """
    Send connect to database.
    """
    db_name = context.conf['dbname']
    context.cli.sendline('use {0}'.format(db_name))


@when('we connect to dbserver')
def step_db_connect_dbserver(context):
    """
    Send connect to database.
    """
    context.cli.sendline('use mysql')


@then('dbcli exits')
def step_wait_exit(context):
    """
    Make sure the cli exits.
    """
    wrappers.expect_exact(context, pexpect.EOF, timeout=5)


@then('we see dbcli prompt')
def step_see_prompt(context):
    """
    Wait to see the prompt.
    """
    user = context.conf['user']
    host = context.conf['host']
    dbname = context.conf['dbname']
    wrappers.expect_exact(context, 'mysql {0}@{1}:{2}> '.format(user, host, dbname), timeout=5)


@then('we see help output')
def step_see_help(context):
    for expected_line in context.fixture_data['help_commands.txt']:
        wrappers.expect_exact(context, expected_line+'\r\n', timeout=1)


@then('we see database created')
def step_see_db_created(context):
    """
    Wait to see create database output.
    """
    wrappers.expect_exact(context, 'Query OK, 1 row affected\r\n', timeout=2)


@then('we see database dropped')
def step_see_db_dropped(context):
    """
    Wait to see drop database output.
    """
    wrappers.expect_exact(context, 'Query OK, 0 rows affected\r\n', timeout=2)


@then('we see database connected')
def step_see_db_connected(context):
    """
    Wait to see drop database output.
    """
    wrappers.expect_exact(context, 'You are now connected to database "', timeout=2)
    wrappers.expect_exact(context, '"', timeout=2)
    wrappers.expect_exact(context, ' as user "{0}"\r\n'.format(context.conf['user']), timeout=2)
