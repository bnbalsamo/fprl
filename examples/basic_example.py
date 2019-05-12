import logging
from uuid import uuid4

import fprl
from flask import Flask, current_app, request

# Init our app
app = Flask("test_app")


@app.route("/")
def hi():
    request.logger.info("Stuff happens")
    return "Hello World!"


# Configure fprl
app.before_request(fprl.inject_logger)


# Configure logging
logging.basicConfig(level="DEBUG")


# Configure some automated logging at request start/end
#
# Note that this additional before_request occurs **after**
# the fprl configuration - so we have access to the logger.
def log_request_completes(resp):
    request.logger.debug("Request complete!")
    return resp


def log_request_begins():
    request.logger.debug("Request begins!")


app.before_request(log_request_begins)
app.after_request(log_request_completes)
