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
    A log handler whose log messages always start at the beginning of a line.

    This class is useful for preventing output like the following during
    unittest runs:

    ........................log: [INFO] foo
    ..................................................

    The stream attribute (i.e. the stream passed to this class's
    constructor) must implement stream.last_char().

    See also CPython issue #16889: http://bugs.python.org/issue16889
    """

    def emit(self, record):
        if self.stream.last_char() != "\n":
            self.stream.write("\n")

        super(NewlineStreamHandler, self).emit(record)
