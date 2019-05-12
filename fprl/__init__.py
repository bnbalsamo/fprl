"""fprl: A library for implementing logs per flask request."""

__author__ = "Brian Balsamo"
__email__ = "Brian@BrianBalsamo.com"
__version__ = "0.0.1"

import logging
from uuid import uuid4

from flask import current_app, request


def inject_logger():
    """
    Injects a logger into each request instance.

    Register this as an app pre_request hook, ideally
    as the first hook so the logger can be utilized by
    later pre_request hooks.

    Utilizes the :func:`fprl.build_logger` callback
    in order to build a logger instance, and
    attaches it to the active request as flask.request.logger
    """
    logger = build_logger()
    request.logger = logger


def build_logger():
    """
    Construct a logger instance.

    This callback is used to build the logger that
    :func:`fprl.inject_logger` attaches to the request proxy.

    This can be overridden to change the behavior
    of the library to utilize other logging libraries.

    This function will be called when the flask request context
    and the flask application context are active, and it will
    be called before **every** request.

    :rtype: logging.Logger
    """
    return _default_build_logger()


def _default_build_logger():
    """
    Provide the default build_logger logic.

    Returns a logger which is a child of the primary
    application logger in the "per_request" namespace
    followed by a uuid4.

    :rtype: logging.Logger
    """
    logger = logging.getLogger(
        "{}.per_request.{}".format(current_app.import_name, uuid4().hex)
    )
    return logger
