# encoding: utf-8

"""
Contains argument-parsing code and command-line documentation.

"""

from __future__ import absolute_import

import argparse
import sys

import pizza
from pizza.scripts.pizza.general.optionparser import (
    Option, ArgParser, UsageError)


METAVAR_INPUT_DIR = 'DIRECTORY'

FLAGS_CHECK_EXPECTED = Option(('--check-output', ))
FLAGS_HELP = Option(('-h', '--help'))
FLAGS_LICENSE = Option(('--license', ))
FLAGS_MODE_TESTS = Option(('--run-tests', ))
FLAGS_SOURCE_DIR = Option(('--dev-source-dir', ))
FLAGS_VERBOSE = Option(('-v', '--verbose'))

# TODO: populate with sample.json description and URL.
DESCRIPTION = """\
Make a pizza!
"""

EPILOG = "This is version %s of Pizza." % pizza.__version__

COPYRIGHT_LINE = "Copyright (C) 2011-2013 Chris Jerdonek. All rights reserved."

LICENSE_STRING = """\
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* The names of the copyright holders may not be used to endorse or promote
  products derived from this software without specific prior written
  permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

# This dict lets us group help strings together for easier editing.
HELP_STRINGS = {
    'args': """\
zero more input values.
""",
    FLAGS_MODE_TESTS: """\
run project tests.  Tests include unit tests and doctests.  If %(metavar)s
arguments are provided, then only tests whose names begin with one of the
strings are run.  Test names begin with the fully qualified module name.
""",
    FLAGS_HELP: """\
show this help message and exit.
""",
}

def _get_version_header():
    return "Molt %s" % pizza.__version__


def get_version_string():
    using_string = "Using: Python %s\n at %s" % (sys.version, sys.executable)
    s = "\n\n".join([_get_version_header(), using_string, COPYRIGHT_LINE])
    return s


def get_license_string():
    s = "\n\n".join([_get_version_header(), COPYRIGHT_LINE, LICENSE_STRING])
    return s


def preparse_args(sys_argv):
    """
    Parse command arguments without raising an exception (or exiting).

    This function allows one to have access to the command-line options
    before configuring logging (in particular before exception logging).

    Returns a Namespace object.

    """
    try:
        # Suppress the help option to prevent exiting.
        ns = parse_args(sys_argv, None, suppress_help_exit=True)
    except UsageError:
        # Any usage error will occur again during the real parse.
        return None
    return ns


def parse_args(sys_argv, suppress_help_exit=False):
    """
    Parse arguments and return a Namespace object.

    Raises UsageError on command-line usage error.

    """
    parser = _create_parser(suppress_help_exit=suppress_help_exit)
    return parser.parse_args(sys_argv[1:])


def _create_parser(suppress_help_exit=False):
    """
    Return an ArgParser for the program.

    """
    parser = ArgParser(description=DESCRIPTION,
                       epilog=EPILOG,
                       add_help=False,
                       # Preserves formatting of the description and epilog.
                       formatter_class=argparse.RawDescriptionHelpFormatter)

    def add_arg(option, help=None, **kwargs):
        """option: an option string or tuple of one or more option strings."""
        if help is None:
            help = HELP_STRINGS[option]
        if isinstance(option, basestring):
            option = (option, )
        parser.add_argument(*option, help=help, **kwargs)

    # TODO: incorporate the METAVAR names into the help messages, as appropriate.
    # TODO: fix the help message.
    add_arg('args', metavar='VALUE', nargs='*')
    # Defaults to the empty list if provided with no names, or else None.
    add_arg(FLAGS_MODE_TESTS, metavar='NAME', dest='test_names', nargs='*')
    # This argument is the path to a source checkout or source distribution.
    # This lets one specify project resources not available in a package
    # build or install, when doing development testing.  Defaults to no
    # source directory.
    add_arg(FLAGS_SOURCE_DIR, metavar='DIRECTORY', dest='source_dir',
            action='store', default=None, help=argparse.SUPPRESS)
    add_arg(FLAGS_LICENSE, dest='license_mode', action='store_true',
            help='print license info to stdout.')
    add_arg(('-V', '--version'), dest='version_mode', action='store_true',
            help='print version info to stdout.')
    add_arg(FLAGS_VERBOSE, dest='verbose', action='store_true',
            help='log verbosely.')
    # We add help manually for more control.
    help_action = "store_true" if suppress_help_exit else "help"
    add_arg(FLAGS_HELP, action=help_action)

    return parser
