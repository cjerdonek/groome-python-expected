"""
Provides the function for the main setup.py console_script.

"""

import logging
import os
import sys
import traceback

import pizza.pizza as _pizza
import pizza.general.common as _common
import pizza.general.logconfig as logconfig
import pizza.general.optionparser as _parsing
import pizza.scripts
import pizza.scripts.pizza.argparsing as argparsing
import pizza.test.harness.main as harness

EXIT_STATUS_SUCCESS = 0
EXIT_STATUS_FAIL = 1
EXIT_STATUS_USAGE_ERROR = 2

LOGGING_LEVEL_DEFAULT = logging.INFO

# TODO [template]: should this be made public with a better name?
log = logging.getLogger("pizza.script")
# Loggers that should display during testing.
# TODO [template]: make this test_loggers instead of test_logger_names.
test_logger_names = [logger.name for logger in (log, harness.log)]


def error(msg, add_trace=False):
    if add_trace:
        msg = traceback.format_exc()
    log.error(msg)


# TODO [template]: make this testable.
# TODO [template]: finish documenting this method.
# TODO [template]: improve parameter names.
def _configure_logging(level=None, stream=None, is_testing=False,
                       is_verbose=False):
    """
    Arguments:

      level: lowest logging level to log.
      stream: the stream to which to log (e.g. sys.stderr).

    """
    if stream is None:
        stream = sys.stderr

    level = logging.DEBUG if is_verbose else LOGGING_LEVEL_DEFAULT

    # We pass a newline as last_text to prevent a newline from being added
    # before the first log message.
    rstream = logconfig.RememberingStream(stream, last_text='\n')
    handler = logconfig.NewlineStreamHandler(rstream)

    if is_testing:
        # Then only log designated test loggers.
        class Filter(object):
            def filter(self, record):
                return record.name in test_logger_names
        handler.addFilter(Filter())
    if not is_verbose:
        # Then shorten the logger name if long.
        class Filter(object):
            def filter(self, record):
                """Set record.truncated_name."""
                parts = record.name.split(".")
                if len(parts) <= 3:
                    truncated_name = record.name
                else:
                    truncated_name = '.'.join(parts[:2] + ['.', parts[-1]])
                record.truncated_name = truncated_name
                return True
        handler.addFilter(Filter())

    # Prefix log messages unobtrusively with "log" to distinguish log
    # messages more obviously from other text sent to the error stream.
    format_string = ("log: %%(%s)s: [%%(levelname)s] %%(message)s" %
                     ('name' if is_verbose else 'truncated_name'))

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    # Adding at least one handler to the root logger prevents the following
    # message from ever being logged:
    # "No handlers could be found for logger..."
    root.addHandler(handler)

    log.debug("debug logging enabled")


def configure_logging(argv, stream=None):
    """
    Configure logging and return whether to run in verbose mode.

    """
    if argv is None:
        argv = sys.argv
    if stream is None:
        stream = sys.stderr

    is_testing = False
    is_verbose = False

    # Configure logging before parsing arguments for real.
    ns = argparsing.preparse_args(argv)

    if ns is not None:
        # Then args parsed without error.
        is_verbose = ns.verbose
        if ns.run_tests:
            is_testing = True

    # TODO [template]: reconsider the argument names here.
    _configure_logging(stream=stream, is_testing=is_testing,
                       is_verbose=is_verbose)

    return is_verbose


def _main_inner(argv, from_source):
    """Run the program and return the status code."""
    argv = list(argv)  # since we'll be modifying this.

    pizza_dir = os.path.dirname(pizza.__file__)

    if from_source:
        # TODO [template]: expose this path calculation in a more central module.
        sdist_dir = os.path.join(pizza_dir, os.pardir)
        argv[1:1] = ['--sdist-dir', sdist_dir]
        start_dir = sdist_dir
    else:
        start_dir = pizza_dir

    log.debug("argv: %r" % argv)
    ns = argparsing.parse_args(argv)
    log.debug("parsed args: %r" % ns)
    log.debug("cwd: %r" % os.getcwd())

    if ns.run_tests is not None:  # Then the value is a list.
        test_argv = ([argv[0], 'discover', '--start-directory', start_dir] +
                     ns.run_tests)
        harness.run_tests(test_argv)
    else:
        values = ns.args
        result = _pizza.run_pizza(values)
        print(result)


def _main(argv=None, from_source=False):
    if argv is None:
        argv = sys.argv

    verbose = configure_logging(argv, stream=sys.stderr)
    # TODO [template]: also handle KeyboardInterrupt?
    try:
        _main_inner(argv, from_source)
        status = EXIT_STATUS_SUCCESS
    except _parsing.UsageError as err:
        details = """\
Usage error: %s
-->argv: %r
Pass %s for help documentation and available options.""" % (
            err, sys.argv, argparsing.OPTION_HELP.display(' or '))
        error(details, verbose)
        status = EXIT_STATUS_USAGE_ERROR
    except _common.Error, err:
        msg = """\
%s
Pass %s for the stack trace.""" % (err,
                                   argparsing.OPTION_VERBOSE.display(' or '))
        error(msg, add_trace=verbose)
        status = EXIT_STATUS_FAIL
    except Exception, err:
        # Always add the stack trace for "unexpected" exceptions.
        error(err, add_trace=True)
        status = EXIT_STATUS_FAIL

    return status


# We follow most of Guido van Rossum's 2003 advice regarding main()
# functions (though we choose _main() as the function that returns an exit
# status rather than main()):
# http://www.artima.com/weblogs/viewpost.jsp?thread=4829
def main(argv=None, from_source=False):
    """
    Arguments:

      from_source: whether this function is being called from a source
        checkout (e.g. by running `python runpizza.py` or
        `python -m pizza.scripts.pizza`).

    """
    status = _main(argv, from_source=from_source)
    sys.exit(status)
