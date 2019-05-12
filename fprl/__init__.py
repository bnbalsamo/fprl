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

    Utilizes the fprl.build_logger
    in order to build a logger instance, and
    attaches it to the active request as flask.request.logger
    """
    logger = build_logger()
    request.logger = logger


def build_logger(*args, **kwargs):
    """
    Construct a logger instance.

    :rtype: logging.Logger
    """
    return _default_build_logger(*args, **kwargs)


def _default_build_logger():
    """Provide the default build_logger logic."""
    logger = logging.getLogger(
        "{}.per_request.{}".format(current_app.import_name, uuid4().hex)
    )
    return logger
