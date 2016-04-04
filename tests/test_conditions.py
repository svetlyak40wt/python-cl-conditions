# coding: utf-8

from unittest import TestCase

from hamcrest import assert_that, contains

from conditions.exceptions import RestartNotFoundError
from conditions import (
    restart,
    restarts,
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

        with restart(choose_bar) as call:
            self.log('Calling foo')
            call(self.foo)

    def test_without_handler(self):
        self.assertRaises(TestError, self.foo)

        assert_that(self.messages,
                    contains('FOO before signal'))

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

    def test_with_handler_for_parent_exception_class(self):
        def continue_execution(e):
            self.log('Continuing execution')

        # in this case, it should work as well
        with handle(RuntimeError, continue_execution):
            self.foo()
            self.bar()

        assert_that(self.messages,
                    contains('FOO before signal',
                             'Continuing execution',
                             'FOO after signal',
                             'BAR'))

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

    def test_when_restart_returns_value(self):
        def use_value(value):
            return value

        def handle_error(e):
            invoke_restart('use_value', 12345)

        def good_function():
            with restart(use_value) as call:
                return call(bad_function)

        def bad_function():
            signal(RuntimeError())

        with handle(RuntimeError, handle_error):
            result = good_function()

        assert result == 12345


    def test_when_multiple_restarts(self):
        def handle_error_using_value(e):
            invoke_restart('use_value', -1)

        def handle_error_trying_value(e):
            invoke_restart('try_value', 5)

        def handle_error_continuing(e):
            invoke_restart('throw', e)

        def good_function(b):
            def use_value(value):
                return value

            def try_value(value):
                return good_function(value)

            def throw(e):
                raise e

            with restarts(use_value,
                          try_value,
                          throw) as call:
                return call(bad_function, 1000, b)

        def bad_function(a, b):
            return a / b

        result = good_function(10)
        assert result == 100

        with handle(ZeroDivisionError, handle_error_using_value):
            result = good_function(0)
            assert result == -1

        with handle(ZeroDivisionError, handle_error_trying_value):
            result = good_function(0)
            assert result == 200

        with handle(ZeroDivisionError, handle_error_continuing):
            self.assertRaises(ZeroDivisionError, good_function, 0)
