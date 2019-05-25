import unittest
from logging import Logger

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


if __name__ == "__main__":
    unittest.main()
