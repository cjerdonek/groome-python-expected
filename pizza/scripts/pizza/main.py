"""
Provides the function for the main setup.py console_script.

"""

import logging
import os
import sys

import pizza.pizza as _pizza
import pizza.scripts
import pizza.scripts.pizza.argparsing as argparsing
import pizza.scripts.pizza.general.logconfig as logconfig
import pizza.test.harness.main as harness


LOGGING_LEVEL_DEFAULT = logging.INFO

# TODO: should this be made public with a better name?
log = logging.getLogger("pizza.script")
# Loggers that should display during testing.
test_logger_names = [logger.name for logger in (log, harness.log)]


# TODO: make this testable.
# TODO: finish documenting this method.
# TODO: improve parameter names.
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

def configure_logging(sys_argv, sys_stderr=None):
    """
    Configure logging and return whether to run in verbose mode.

    """
    if sys_stderr is None:
        sys_stderr = sys.stderr

    is_testing = False
    is_verbose = False

    # Configure logging before parsing arguments for real.
    ns = argparsing.preparse_args(sys_argv)

    if ns is not None:
        # Then args parsed without error.
        is_verbose = ns.verbose
        if ns.run_tests:
            is_testing = True

    # TODO: reconsider the argument names here.
    _configure_logging(stream=sys_stderr, is_testing=is_testing,
                       is_verbose=is_verbose)

    return is_verbose, sys_stderr

def main_inner(sys_argv=None, from_source=False):
    """Run the program and return the status code."""
    if sys_argv is None:
        sys_argv = sys.argv
    sys_argv = list(sys_argv)  # since we'll be modifying this.

    verbose, stderr_stream = configure_logging(sys_argv)

    pizza_dir = os.path.dirname(pizza.__file__)

    if from_source:
        # TODO: expose this path calculation in a more central module.
        sdist_dir = os.path.join(pizza_dir, os.pardir)
        sys_argv[1:1] = ['--sdist-dir', sdist_dir]
        start_dir = sdist_dir
    else:
        start_dir = pizza_dir

    # TODO: add the try-except from Molt.

    log.debug("argv: %r" % sys_argv)
    ns = argparsing.parse_args(sys_argv)
    log.debug("parsed args: %r" % ns)
    log.debug("cwd: %r" % os.getcwd())

    if ns.run_tests is not None:  # Then it is a list.
        test_argv = ([sys_argv[0], 'discover', '--start-directory',
                      start_dir] + ns.run_tests)
        harness.run_tests(test_argv)
    else:
        values = ns.args
        result = _pizza.run(values)
        print(result)

    # TODO: return the right status code as appropriate.
    return 0

# TODO: follow all of the recommendations here:
# http://www.artima.com/weblogs/viewpost.jsp?thread=4829
# Keep this link for reference even after following the guidance.
def main(sys_argv=None, from_source=False, **kwargs):
    """
    Arguments:

      from_source: whether this function is being called from a source
        checkout (e.g. by running `python test_molt.py` or
        `python -m molt.scripts.molt`).

    """
    status = main_inner(sys_argv, from_source=from_source)
    sys.exit(status)
