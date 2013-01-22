# encoding: utf-8
#
# Copyright (C) 2011-2012 Chris Jerdonek. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * The names of the copyright holders may not be used to endorse or promote
#   products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

"""
Supports logging configuration.

"""

import logging
import os
import sys

_log = logging.getLogger(__name__)


class RememberingStream(object):

    """
    A stream that "remembers" the last text sent to write().

    """

    def __init__(self, stream, last_text=''):
        self._stream = stream
        self._last_text = last_text

    def last_char(self):
        if self._last_text:
            return self._last_text[-1]

    def write(self, text):
        if not text:
            return
        self._stream.write(text)
        self._last_text = text

    # A flush() method is needed to be able to pass instances of this
    # class to unittest.TextTestRunner's constructor.
    def flush(self):
        self._stream.flush()

class NewlineStreamHandler(logging.StreamHandler):

    """
    A logging handler that begins log messages with a newline if needed.

    This class is useful for preventing messages logged during test runs
    from displaying at the end of a line of dots "......".

    The stream attribute (i.e. the stream passed to this class's
    constructor) must implement stream.last_char().

    """

    def emit(self, record):
        if self.stream.last_char() != "\n":
            self.stream.write("\n")

        super(NewlineStreamHandler, self).emit(record)


# TODO: make this testable.
# TODO: finish documenting this method.
# TODO: improve parameter names.
# TODO: consider using filters instead of passing explicit loggers.
def configure_logging(logging_level, persistent_loggers=None,
                      stderr_stream=None, test_config=False):
    """
    Configure logging.

    If in test mode, adds a null handler to the root logger to prevent the
    following message from being written while running tests:

      'No handlers could be found for logger...'

    Arguments:

      persistent_loggers: the loggers that should always log.

    """
    if stderr_stream is None:
        stderr_stream = sys.stderr

    root_logger = logging.getLogger()  # the root logger.
    root_logger.setLevel(logging_level)
    #root_logger.addHandler(logging.NullHandler())

    class Filter(object):
        def filter(self, record):
            name = record.name
            if name.startswith("pizza.scripts"):
                return True
            return False

    #root_logger.addFilter(filt)

    if test_config:
        # Then configure log messages to be swallowed by default.
        # TODO: is this necessary?
        handler = logging.NullHandler()
        root_logger.addHandler(handler)

        # Set the loggers to display during test runs.
        visible_loggers = [_log] + persistent_loggers
    else:
        temp_log = logging.getLogger("pizza.temp")
        visible_loggers = [root_logger]

    # Prefix log messages unobtrusively with "log" to distinguish log
    # messages more obviously from other text sent to the error stream.
    format_string = "log: %(name)s: [%(levelname)s] %(message)s"
    formatter = logging.Formatter(format_string)

    handler = NewlineStreamHandler(stderr_stream)
    handler.setFormatter(formatter)
    handler.addFilter(Filter())

    for logger in visible_loggers:
        logger.addHandler(handler)

    _log.debug("Debug logging enabled.")
    temp_log.error("testing...")
    _log.debug("Visible loggers: %s" % repr([logger.name for logger in visible_loggers]))
