# coding: utf-8

from unittest import TestCase

from hamcrest import assert_that, contains

from conditions.exceptions import RestartNotFoundError
from conditions import (
    restart,
    handle,
    signal,
    invoke_restart)


class TestError(RuntimeError):
    pass


class HandlerTests(TestCase):
    messages = []

    def log(self, message):
        self.messages.append(message)

    def setUp(self):
        self.messages[:] = []


    def foo(self):
        self.log('FOO before signal')
        signal(TestError())
        self.log('FOO after signal')

    def bar(self):
        self.log('BAR')

    def blah(self):
        def choose_bar():
            self.log('Calling bar instead of failed foo')
            self.bar()

        with restart('choose_bar', choose_bar):
            self.log('Calling foo')
            self.foo()

    def test_with_handler(self):
        def continue_execution(e):
            self.log('Continuing execution')

        with handle(TestError, continue_execution):
            self.foo()
            self.bar()

        assert_that(self.messages,
                    contains('FOO before signal',
                             'Continuing execution',
                             'FOO after signal',
                             'BAR'))

    def test_without_handler(self):
        self.assertRaises(TestError, self.foo)

        assert_that(self.messages,
                    contains('FOO before signal'))

    def test_with_restarts(self):
        def choose_bar(e):
            invoke_restart('choose_bar')

        with handle(TestError, choose_bar):
            self.blah()

        assert_that(self.messages,
                    contains(
                        'Calling foo',
                        'FOO before signal',
                        'Calling bar instead of failed foo',
                        'BAR'))


    def test_when_restart_not_found(self):
        def choose_bar(e):
            invoke_restart('some_strange_restart')

        with handle(TestError, choose_bar):
            self.assertRaises(RestartNotFoundError, self.blah)

        assert_that(self.messages,
                    contains(
                        'Calling foo',
                        'FOO before signal'))
