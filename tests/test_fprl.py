import unittest

from flask import Flask, request

import fprl


def get_app():
    app = Flask("test_app")

    @app.route("/")
    def hi():
        request.logger.info("hi!")
        return "Hello World!"

    return app


class Tests(unittest.TestCase):
    def setUp(self):
        # Perform any setup that should occur
        # before every test
        self.app = get_app()
        self.app.before_request(fprl.inject_logger)
        self.client = self.app.test_client()

    def tearDown(self):
        # Perform any tear down that should
        # occur after every test
        del self.client
        del self.app

    def testPass(self):
        self.assertEqual(True, True)

    def testVersionAvailable(self):
        x = getattr(fprl, "__version__", None)
        self.assertTrue(x is not None)

    def testGet(self):
        self.client.get("/")


if __name__ == "__main__":
    unittest.main()
