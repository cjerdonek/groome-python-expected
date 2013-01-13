# coding: utf-8

"""

Instructions for Maintainers
============================



1. Update the long_description file
-----------------------------------

The long_description argument to setup() is stored in a source file.
Update and commit this file before pushing to PyPI.  To update the file:

    python setup.py prep

This writes the long description to setup_long_description.rst.  Then commit
this file to the repository.

You must have pandoc installed to run the prep command:

    http://johnmacfarlane.net/pandoc/

It helps to check the long_description file prior to pushing to PyPI because
if PyPI encounters any problems, it will render the long description as
plain-text instead of as HTML.  To check the file, convert it to HTML yourself
using the same process that PyPI uses.  After installing Docutils
(http://docutils.sourceforge.net/), run--

    $ python setup.py --long-description | rst2html.py --no-raw > temp.html

Also see:

  http://docs.python.org/dev/distutils/uploading.html#pypi-package-display
  http://bugs.python.org/issue15231

You can also view the long description file on GitHub as a sanity check.

"""


# We use setuptools/Distribute because distutils does not seem to support
# the following arguments to setUp().  Passing these arguments to
# setUp() causes a UserWarning to be displayed.
#
#  * entry_points
#  * install_requires
#

# Distribute/setuptools does not expose all distutils classes.
from distutils.cmd import Command
# We use distutils's upload command because Distribute's seems not to
# work as well in certain circumstances.  For example, see the following
# Distribute bug reports:
#
#   https://bitbucket.org/tarek/distribute/issue/346
#   https://bitbucket.org/tarek/distribute/issue/348
#
from distutils.command.upload import upload as _upload
import logging
import os
import sys

import pizza_setup.utils as utils

dist_version = None

# TODO: explore whether I can support distutils (at least for end-users).
# This boolean is temporary for more convenient testing/experimentation.
USE_DISTRIBUTE = True

if USE_DISTRIBUTE:
    # Distribute does not seem to support the -r/--repository option
    # with the register command (at least without a [server-login] section
    # in the .pypirc).  See Distribute issue #346 :
    # https://bitbucket.org/tarek/distribute/issue/346/upload-fails-without-server-login-but
    import setuptools
    from setuptools.command.register import register as _register
    setup = setuptools.setup
    dist = setuptools
    import pkg_resources  # included with Distribute.
    # This is different from setuptools.__version__, which is always '0.6'.
    dist_version = pkg_resources.get_distribution("distribute").version
else:
    from distutils.command.register import register as _register
    from distutils.core import setup
    dist = distutils

PACKAGE_NAME = 'pizza'

README_PATH = 'README.md'
HISTORY_PATH = 'HISTORY.md'
LONG_DESCRIPTION_PATH = 'setup_long_description.rst'

_log = logging.getLogger(os.path.basename(__file__))


def configure_logging():
    """
    Configure logging with simple settings.

    """
    # Prefix the log messages to distinguish them from other text sent to
    # the error stream.
    format_string = ("%s: %%(name)s: [%%(levelname)s] %%(message)s" %
                     PACKAGE_NAME)

    logging.basicConfig(format=format_string, level=logging.INFO)

    _log.debug("Debug logging enabled.")


def prompt(command):
    command_name = command.get_command_name()
    # The repository attribute is the URL.
    answer = raw_input("Are you sure you want to %s to %s (yes/no)? " %
                       (command_name, command.repository))
    if answer != "yes":
        sys.exit("aborted: %s" % command_name)


def get_long_description():
    path = LONG_DESCRIPTION_PATH
    try:
        long_description = utils.read(path)
    except IOError:
        if not os.path.exists(path):
            raise Exception("Long-description file not found at: %s\n"
                            "  You must first run the command: %s\n"
                            "  See the docstring of this module for details." % (path, COMMAND_PREP))
        raise
    return long_description


## New and customized setup() commands.
##
## For commands that write to PyPI, we customize them to prompt with the
## URL before writing to PyPI.

class upload(_upload):
    def run(self):
        prompt(self)
        return _upload.run(self)

class register(_register):
    # We override post_to_server() instead of run() because finalize_options()
    # and self._set_config() are called at the beginning of run().
    def post_to_server(self, data, auth=None):
        prompt(self)
        return _register.post_to_server(self, data, auth=auth)

class prep(Command):
    """
    Prepare a release for pushing to PyPI.

    In particular, this updates the long_description file, which should
    be committed prior to pushing to PyPI.

    """

    description = ("prepare a release for pushing to PyPI")

    # Attributes and methods required by distutils.
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        utils.update_description_file([README_PATH, HISTORY_PATH],
                                      LONG_DESCRIPTION_PATH,
                                      docstring_path=__file__)


CLASSIFIERS = (
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: PyPy',
)

PACKAGES = [
    'pizza',
    'pizza.scripts',
    'pizza.scripts.pizza',
    'pizza.scripts.pizza.general',
    # The following packages are only for testing.
    'pizza.test',
    'pizza.test.harness',
    'pizza.test.pizza',
]

def main(sys_argv):
    """
    Call setup() with the correct arguments.

    """
    configure_logging()
    package_dir = os.path.join(os.path.dirname(__file__), PACKAGE_NAME)
    version = utils.scrape_version(package_dir)

    _log.info("running version: %s" % version)
    _log.info("using: version %s (%s) of %s" %
              (repr(dist.__version__), dist_version, repr(dist)))

    long_description = get_long_description()

    setup(name='Pizza',
          cmdclass = {'pizza_prep': prep,
                      'register': register,
                      'upload': upload},
    #      install_requires=INSTALL_REQUIRES,
          packages=PACKAGES,
          long_description=long_description,
    #      package_data=package_data,
          entry_points = {
            'console_scripts': [
                'pizza=pizza.scripts.pizza.main:main',
            ],
          },
          classifiers=CLASSIFIERS,
          version=version,
    )

if __name__=='__main__':
    main(sys.argv)
