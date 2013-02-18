# encoding: utf-8

"""
Contains argument-parsing code and command-line documentation.

"""

import argparse
import sys

import pizza
import pizza.general.optionparser as _parsing

METAVAR_ARG_VALUE = 'VALUE'
METAVAR_INPUT_DIR = 'DIRECTORY'

# TODO [template]: rename to OPTION_*...
OPTION_HELP = _parsing.Option(('-h', '--help'))
FLAGS_LICENSE = _parsing.Option(('--license',))
FLAGS_MODE_TESTS = _parsing.Option(('-T', '--run-tests',))
FLAGS_SDIST_DIR = _parsing.Option(('--sdist-dir',))
OPTION_VERBOSE = _parsing.Option(('-v', '--verbose'))

# TODO [template]: populate with sample.json description and URL.
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
discover and run project tests.  Tests include unit tests and doctests.
Running this command is for the most part equivalent to running unittest's
command-line discover command with an appropriate -t/--start-directory value.
Option values are passed along as is to the discover command.  For info on
the discovery options, consult the Python documentation or pass -h or --help
as an option to this value.
""",
    FLAGS_SDIST_DIR: """\
the path to the source distribution directory (aka sdist) if running
from a source checkout.  Otherwise, this option should be left out.
""",
    OPTION_HELP: """\
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

    Returns a Namespace object, or None if UsageError.

    """
    try:
        # Suppress the help option to prevent exiting.
        ns = parse_args(sys_argv, suppress_help_exit=True)
    except _parsing.UsageError:
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
    parser = _parsing.ArgParser(description=DESCRIPTION,
                       epilog=EPILOG,
                       add_help=False,
                       # Preserves formatting of the description and epilog.
                       formatter_class=argparse.RawDescriptionHelpFormatter)

    def add_arg(obj, option, help=None, **kwargs):
        """
        Arguments:
          obj: a parser or group.
          option: an option string or tuple of one or more option strings.

        """
        if help is None:
            help = HELP_STRINGS[option]
        if isinstance(option, basestring):
            option = (option, )
        obj.add_argument(*option, help=help, **kwargs)

    # TODO [template]: incorporate the METAVAR names into the help messages,
    # as appropriate.
    # TODO [template]: fix the help message.
    add_arg(parser, 'args', metavar=METAVAR_ARG_VALUE, nargs='*')
    # This argument is the path to a source checkout or source distribution.
    # This lets one specify project resources not available in a package
    # build or install, when doing development testing.  Defaults to no
    # source directory.
    add_arg(parser, FLAGS_SDIST_DIR, metavar='DIRECTORY', dest='sdist_dir',
            action='store', default=None)
    add_arg(parser, OPTION_VERBOSE, dest='verbose', action='store_true',
            help='log verbosely.')

    # This group corresponds to the possible "modes" or "commands".
    # We do not use a subparsers for this because of issue #17050:
    # http://bugs.python.org/issue17050
    group = parser.add_mutually_exclusive_group()
    # run_tests is None if not provided, otherwise a list.
    add_arg(group, FLAGS_MODE_TESTS, dest='run_tests',
            nargs=argparse.REMAINDER)
    add_arg(group, FLAGS_LICENSE, dest='license_mode', action='store_true',
            help='print license info to stdout.')
    add_arg(group, ('-V', '--version'), dest='version_mode',
            action='store_true', help='print version info to stdout.')
    # We add help manually for more control.
    help_action = "store_true" if suppress_help_exit else "help"
    add_arg(group, OPTION_HELP, action=help_action)

    return parser
