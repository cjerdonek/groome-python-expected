How to release Pizza
====================

This document contains step-by-step instructions for Pizza maintainers on
how to release the first version and new versions of Pizza.  For
installation and usage instructions, consult the README or the
[project page](https://github.com/cjerdonek/groome-python-expected).


Background
----------

The release process documented here assumes that you have already installed
[Distribute](http://pypi.python.org/pypi/distribute).  We recommend version
0.6.34 or higher since these instructions were written using that version.

Distribute is an extension of the Python standard library's
[distutils](http://docs.python.org/distutils/index.html) module with
some added features.  Distribute shows up as a module called `setuptools`
since Distribute is a replacement of an older module called `setuptools`.

For basic background information on `setup.py` and related concepts,
consult the `distutils` and Distribute documentation linked to above.
Also look at the `setup.py` source code to see how things are done.


Releasing a new version
-----------------------

This section walks maintainers through the steps you should take to deploy
a new release of this project to PyPI (pypi.python.org).


* prerequisite: get a PyPI account and make sure you have permissions

### 1. Finalize the code

Make sure the code is finalized: that the tests pass, the version number
in the package's __init__.py is bumped, the HISTORY file is updated,
MANIFEST.in is updated, etc.

For versioning your project, you may want to consider semantic versioning:
http://semver.org.

Regarding the manifest file, MANIFEST.in is a file that tells setup.py
what files to include in your source distribution, in addition to any
Python files automatically included.  A source distribution is probably what you'll want
to upload to PyPI.

The
setup.py script's sdist command generates the source distribution as a
zipped file.

Note that unlike
distutils, Distribute does not include package_data in the sdist, no matter
what the include_package_data argument passed to setup() is.  See the
following Distribute issue, for example:

https://bitbucket.org/tarek/distribute/pull-request/4

To assist you in checking that MANIFEST.in is correct and up to date, after
generating the sdist, this module's sdist command prints a report of how
the project directory differs from the created sdist directory.


### Update the long_description file

The long_description argument to setup() is stored in a source file.
Update and commit this file before pushing to PyPI.  To update the file:

    python setup.py pizza_prep

This writes the long description to setup_long_description.rst.  Then commit
this file to the repository.

You must have pandoc installed to run the pizza_prep command:

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


### 3. Merge your code

Make sure your code is checked in and merged to the right branch.


TODO:

* .pypirc file (include example and recommendation of test server)
  - mention that server-login needed only for Distribute
  - mention bug re: not having server-login

* register

* upload

* Tag your commit and push your tag.

