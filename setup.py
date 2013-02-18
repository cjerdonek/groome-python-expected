#!/usr/bin/env python
# coding: utf-8

"""
Standard Python setup script to support distribution-related tasks.

For instructions on releasing Pizza and on how to use this script, consult
the `releasing.md` file in the `docs` folder of a source distribution.  For
installation and usage instructions, consult the README or the project page:

https://github.com/cjerdonek/groome-python-expected

"""

DISTUTILS_DEBUG = False
# This is a hack to make it easier to enable distutils's debug mode.  This
# code must come before importing from distutils.  See also:
# http://docs.python.org/2/distutils/setupscript.html#debugging-the-setup-script
import os
os.environ['DISTUTILS_DEBUG'] = "1" if DISTUTILS_DEBUG else ""

# We use setuptools/Distribute because distutils does not seem to support
# the following arguments to setUp().  Passing these arguments to
# setUp() causes a UserWarning to be displayed.
#
#  * entry_points
#  * install_requires
#

import distutils
# Distribute/setuptools does not expose all distutils classes.
from distutils.cmd import Command
# We use distutils's upload command because Distribute's seems not to
# work as well in certain circumstances.  For example, see the following
# Distribute bug reports:
#
#   https://bitbucket.org/tarek/distribute/issue/346
#   https://bitbucket.org/tarek/distribute/issue/348
#
import distutils.command.upload as upload_mod
import filecmp
import fnmatch
import logging
import os
import sys

# For various reasons, we deliberately avoid importing from the pizza package
# itself and making the pizza setup code dependent on pizza.  However, it
# is of course okay to import from pizza_setup.
import pizza_setup.utils as utils

# TODO [template]: explore whether I can support distutils (at least for installers).
#
# Whether to use Distribute (or setuptools if not available) over distutils.
# This boolean is temporary for more convenient testing/experimentation.
USE_SETUPTOOLS = True
dist_version = None

if USE_SETUPTOOLS:
    # Distribute does not seem to support the -r/--repository option
    # with the register command (at least without a [server-login] section
    # in the .pypirc).  See Distribute issue #346 :
    # https://bitbucket.org/tarek/distribute/issue/346/upload-fails-without-server-login-but
    import setuptools
    import setuptools.command.register as register_mod
    import setuptools.command.sdist as sdist_mod
    import pkg_resources  # included with Distribute.
    try:
        # This is different from setuptools.__version__, which is always '0.6'
        # in the case of Distribute.
        dist_version = pkg_resources.get_distribution("distribute").version
    except pkg_resources.DistributionNotFound:
        # This is needed to support setuptools if Distribute is not available.
        dist_version = pkg_resources.get_distribution("setuptools").version
    setup = setuptools.setup
    dist = setuptools
else:
    import distutils.command.register as register_mod
    import distutils.command.sdist as sdist_mod
    import distutils.core
    setup = distutils.core.setup
    dist = distutils

PACKAGE_NAME = 'pizza'

README_PATH = 'README.md'
HISTORY_PATH = 'HISTORY.md'
TEMP_DIR = 'temp'
LONG_DESCRIPTION_PATH = 'setup_long_description.rst'
# Top-level names to skip when displaying sdist differences.
SDIST_NAMES_TO_SKIP = ('.git', '.tox', 'build', 'dist', 'temp')

_log = logging.getLogger(os.path.basename(__file__))


def configure_logging():
    """
    Configure setup.py logging with simple settings.

    """
    # Prefix the log messages to distinguish them from other text sent to
    # the error stream.
    format_string = ("%s: %%(name)s: [%%(levelname)s] %%(message)s" %
                     PACKAGE_NAME)
    logging.basicConfig(format=format_string, level=logging.INFO)
    _log.debug("Debug logging enabled.")


def error(msg):
    """
    Exit with an error message

    """
    _log.error(msg)
    sys.exit(1)


def get_long_description():
    path = LONG_DESCRIPTION_PATH
    try:
        long_description = utils.read(path)
    except IOError:
        if not os.path.exists(path):
            raise Exception("long_description file missing: %s" % path)
        raise
    return long_description


def write_long_description(target_path):
    utils.update_description_file([README_PATH, HISTORY_PATH],
                                  target_path,
                                  docstring_path=__file__)

def check_long_description():
    """
    Check whether the prep command needs to be run.

    """
    description_path = LONG_DESCRIPTION_PATH
    temp_path = utils.make_temp_path(description_path, temp_dir=TEMP_DIR)
    write_long_description(temp_path)

    if not filecmp.cmp(temp_path, description_path, shallow=False):
        error("""\
long_description out of date: %s
To update, run the following command and commit the changes--

    python setup.py %s
""" % (description_path, pizza_prep.__name__))

    print("long_description is current: %s" % description_path)


class Reporter(object):

    def __init__(self, project_dir, sdist_dir):
        self.project_dir = project_dir
        self.sdist_dir = sdist_dir

    def make_report(self):
        """
        Display how the sdist differs from the project directory.

        """
        def skip(path):
            dir_path, base_name = os.path.split(path)
            if (base_name.endswith('.pyc') or
                base_name in ('__pycache__', '.DS_Store')):
                return True
            # distutils puts the temporary sdist directory (the directory from
            # which it builds the compressed sdist) into the source tree.
            if path in SDIST_NAMES_TO_SKIP or path == self.sdist_dir:
                return True
            return False

        return utils.describe_differences(self.project_dir, self.sdist_dir,
                                          skip=skip)

    def show_report(self, report, archives, egg_dirs):
        display = """\

Listing unexpected differences between directories--

  project: %s
  sdist: %s (now in %s)

%s
""" % (self.project_dir, self.sdist_dir, archives, report)

        if egg_dirs:
            # For more information on this, see:
            # https://bitbucket.org/tarek/distribute/issue/350
            display += """\

Note: Since an egg-info directory was present when running this command,
the sdist may not reflect recent changes to MANIFEST.in.  Delete the
following egg-info directory and rerun for an up-to-date listing:
%r""" % egg_dirs
        print(display)


# New and customized setup() commands
#
# For commands that write to PyPI, we add a user prompt displaying the URL
# to reduce the chance of accidentally writing to the real PyPI.

class CommandMixin(object):
    def confirm_repository(self):
        command_name = self.get_command_name()
        # The repository attribute is the URL.
        answer = raw_input("Are you sure you want to %s to %s (yes/no)? " %
                           (command_name, self.repository))
        if answer != "yes":
            error("aborted command: %s" % command_name)

class upload(upload_mod.upload, CommandMixin):
    def run(self):
        check_long_description()
        self.confirm_repository()
        return upload_mod.upload.run(self)

class register(register_mod.register, CommandMixin):
    # We override post_to_server() instead of run() because finalize_options()
    # and self._set_config() are called at the beginning of run().
    def post_to_server(self, data, auth=None):
        check_long_description()
        self.confirm_repository()
        return register_mod.register.post_to_server(self, data, auth=auth)

# This command differs from the original by displaying a report showing
# differences between the project repository and the source distribution.
# This is useful in double-checking MANIFEST.in.
class sdist(sdist_mod.sdist):
    def run(self):
        # Check for the presence of a project "egg-info" directory since
        # this can mask what the current MANIFEST.in yields.
        egg_dirs = fnmatch.filter(os.listdir(os.curdir), '*.egg-info')

        # We repeat some of distutils's sdist.make_distribution() logic here.
        _saved_keep_temp = self.keep_temp
        # Tell make_distribution() not to delete the release tree from
        # which it will create the zipped sdist.
        self.keep_temp = True
        sdist_mod.sdist.run(self)
        base_dir = self.distribution.get_fullname()
        reporter = Reporter(project_dir=os.curdir, sdist_dir=base_dir)
        try:
            report = reporter.make_report()
        finally:
            self.keep_temp = _saved_keep_temp
            if not self.keep_temp:
                distutils.dir_util.remove_tree(base_dir, dry_run=self.dry_run)
        _log.info("Wrote archive to: %s" % self.archive_files)
        reporter.show_report(report, self.archive_files, egg_dirs)


class pizza_prep(Command):
    """
    Prepare the project for pushing to PyPI.

    In particular, this updates the long_description file, which should
    be committed prior to pushing to PyPI.

    """
    description = ("prepare the project for pushing to PyPI")

    # Attributes and methods required by distutils.
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        write_long_description(LONG_DESCRIPTION_PATH)


# The purpose of this function is to follow the guidance suggested here:
# http://packages.python.org/distribute/python3.html#note-on-compatibility-with-setuptools
#
# The guidance is for better compatibility when using setuptools (e.g. with
# earlier versions of Python 2) instead of Distribute, because of new
# keyword arguments to setup() that setuptools may not recognize.
def get_extra_args():
    """
    Return a dictionary of extra args to pass to setup().

    """
    extra = {}
    # TODO [template]: document that Distribute is necessary if using Python 3 and
    # possibly include this in the exception message.
    # Check the Python version instead of whether we're using Distribute or
    # setuptools because the former is less brittle.
    if sys.version_info >= (3, ):
        # Causes 2to3 to be run during the build step.
        extra['use_2to3'] = True

    return extra

CLASSIFIERS = (
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: Implementation :: PyPy',
)

def main(sys_argv):
    """
    Call setup() with the correct arguments.

    """
    configure_logging()
    package_dir = os.path.join(os.path.dirname(__file__), PACKAGE_NAME)
    version = utils.scrape_version(package_dir)

    _log.info("running version: %s" % version)
    _log.info("using: version %r (%s) of %r" % (dist.__version__,
                                                dist_version, dist))

    long_description = get_long_description()
    extra_args = get_extra_args()
    # We do not include pizza_setup to prevent it from going into the
    # build/install.  However, this does not prevent it from going into the
    # source distribution, where it should go (which we do via the
    # MANIFEST.in file).  Also, we currently include the test subpackages.
    # For information on excluding test packages, see:
    # http://packages.python.org/distribute/setuptools.html#using-find-packages
    # TODO [template]: add a tox test to check that pizza_setup is not installed.
    packages = setuptools.find_packages(exclude=['pizza_setup',
                                                 'pizza_setup.*'])

    if extra_args:
        _log.info('including extra kwargs: %r' % extra_args)

    setup(name='Pizza',
          version=version,
          description='a model project for a Python command-line script',
          long_description=long_description,
          keywords='project template groome molt pystache mustache',
          author='Chris Jerdonek',
          author_email='chris.jerdonek@gmail.com',
          url='https://github.com/cjerdonek/groome-python-expected',
          packages=packages,
          classifiers=CLASSIFIERS,
          cmdclass = {pizza_prep.__name__: pizza_prep,
                      'register': register,
                      'sdist': sdist,
                      'upload': upload},
    #      install_requires=INSTALL_REQUIRES,
    #      package_data=package_data,
          entry_points = {
            'console_scripts': [
                'pizza=pizza.scripts.pizza.main:main',
            ],
          },
          **extra_args
    )

if __name__=='__main__':
    main(sys.argv)
