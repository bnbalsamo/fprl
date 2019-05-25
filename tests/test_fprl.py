import unittest
from logging import Logger
from unittest import mock

from flask import Flask, request

import fprl


def get_app():
    app = Flask("test_app")

    @app.route("/")
    def hi():
        request.logger.info("hi!")
        return "Hello World!"

    app.before_request(fprl.inject_logger)

    return app


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = get_app()
        self.app.before_request(fprl.inject_logger)
        self.client = self.app.test_client()

    def tearDown(self):
        del self.client
        del self.app

    def testVersionAvailable(self):
        x = getattr(fprl, "__version__", None)
        self.assertTrue(x is not None)

    def testGet(self):
        self.client.get("/")

    def testLoggerCreation(self):
        with self.app.test_request_context("/"):
            self.app.preprocess_request()
            self.assertIsInstance(request.logger, Logger)

    def testLoggersAreDifferentPerRequest(self):
        with self.app.test_request_context("/"):
            self.app.preprocess_request()
            first_logger = request.logger
        with self.app.test_request_context("/"):
            self.app.preprocess_request()
            second_logger = request.logger
        self.assertIsInstance(first_logger, Logger)
        self.assertIsInstance(second_logger, Logger)
        self.assertNotEqual(first_logger, second_logger)

    def testInjectLoggerCalled(self):
        # We can't use the "standard" app provided via
        # setUp here because we need to register the fprl
        # callback _after_ mocking the function.
        app = Flask("test_app")

        @app.route("/")
        def hi():
            request.logger.info("hi!")
            return "Hello World!"

        with mock.patch("fprl.inject_logger") as m:
            app.before_request(fprl.inject_logger)
            with app.test_request_context("/"):
                app.preprocess_request()
            m.assert_called()

    def testBuildLoggerCalled(self):
        with mock.patch("fprl.build_logger") as m:
            self.app.before_request(fprl.inject_logger)
            with self.app.test_request_context("/"):
                self.app.preprocess_request()
            m.assert_called()


if __name__ == "__main__":
    unittest.main()
