import datetime
import logging
from uuid import uuid4

import fprl
import structlog
from flask import Flask, current_app, request


def build_structlog_logger():
    logger = structlog.get_logger("{}.per_request".format(current_app.import_name))
    logger = logger.bind(request_id=uuid4().hex)
    if int(datetime.datetime.now().isoformat()[-1]) % 2 == 0:
        logger.bind(demo="Bind per request!")
    return logger


# Init our app
app = Flask("test_app")


@app.route("/")
def hi():
    request.logger.info("Stuff happens", stuff=[1, 2, 3])
    return "Hello World!"


# Configure fprl
# Override the fprl.build_logger call to return a
# structlog instance of a stdlib logger.
fprl.build_logger = build_structlog_logger
# Hook
app.before_request(fprl.inject_logger)


# Configure logging/structlog
logging.basicConfig(level="INFO")
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(),
        structlog.processors.JSONRenderer(indent=2, sort_keys=True),
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
)


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
