Releasing Pizza
===============

This document contains detailed step-by-step instructions for Pizza maintainers
on how to release both the first version and new versions of Pizza.
For instructions on installing or using the application, or for instructions
on contributing, consult the README or
[project page](https://github.com/cjerdonek/groome-python-expected) instead.

Table of contents:

1.  Background
2.  One-time setup
    * 2.1. Set up PyPI user accounts
    * 2.2. Create `.pypirc` file
3.  Releasing a new version
    * 3.1. Finalize source
      * 3.1.1. Review issues
      * 3.1.2. Update HISTORY file
      * 3.1.3. Double-check the `sdist`
      * 3.1.4. Bump version number
      * 3.1.5. Update `long_description` file
      * 3.1.6. Make sure tests pass
    * 3.2. Merge to release branch, if necessary
    * 3.3. Register version on PyPI
    * 3.4. Upload version to PyPI
    * 3.5. Tag the commit


1. Background
-------------

This document explains how to distribute Pizza via the Python Package Index,
or [PyPI](http://pypi.python.org/pypi) (pronounced Pie-pee-EYE).  Correctly
putting your project on PyPI lets users install your project simply by typing:

    $ pip install pizza

See the [PyPI documentation](http://docs.python.org/distutils/packageindex.html)
on the Python web site for more information on PyPI.

The release process documented here assumes that you have already installed
[Distribute](http://pypi.python.org/pypi/distribute).  We recommend version
0.6.34 or higher since these instructions were tested with that version.

Distribute is an extension of the Python standard library's
[distutils](http://docs.python.org/distutils/index.html) module with
some added features.  Distribute shows up as a module called `setuptools`
since Distribute is a replacement of an older module called `setuptools`.
For basic background information on `setup.py` and related concepts,
consult the `distutils` and Distribute documentation linked to above.

Also look at the project's `setup.py` file to see how things work.  As time
goes on, you should feel free to modify `setup.py` and its supporting code
to better suit the project's needs.


2. One-time setup
-----------------

This section describes setup steps that you need to do only once.


### 2.1. Set up PyPI user accounts

Create a user account on PyPI if you do not already have one, as well as
a test user account.

If Pizza already exists on PyPI, you will also need write permissions on that
project (i.e. to have the "Maintainer" or "Owner" role for the project).
A current project owner can grant you those permissions.

We also recommend creating a user account on the
[test PyPI server](http://testpypi.python.org/pypi).  The test server lets
you try things out, though the server is not always up.  The `-r/--repository`
option to `setup.py` (which we describe below) lets you designate this server.


### 2.2. Create `.pypirc` file

The [`.pypirc` file](http://docs.python.org/dev/distutils/packageindex.html#the-pypirc-file)
is a plain-text configuration file that stores your PyPI credentials.  The
`setup.py` script uses it when you interact with PyPI via the command-line.
We recommend starting out with a `.pypirc` file like the following, which
also enables access to the test server.  The file should be placed in your
home directory:

    [server-login]
    username: <username>
    password: <password>

    [distutils]
    index-servers =
        pypi
        test

    [pypi]
    repository: http://pypi.python.org/pypi
    username: <username>
    password: <password>

    [test]
    repository: http://testpypi.python.org/pypi
    username: <username>
    password: <password>

The `[server-login]` section is needed for increased compatibility
with Distribute.  Without it, Distribute doesn't always work.  For example,
see this Distribute
[bug report](https://bitbucket.org/tarek/distribute/issue/346/upload-fails-without-server-login-but).


3. Releasing a new version
--------------------------

This section describes in detail the steps to release a new version of Pizza,
assuming the above setup steps have been followed.


### 3.1. Finalize source

This section describes steps to prepare the source code for release.  Most
of these steps involve committing changes to files.

In many workflows, the source code is normally in a non-release branch at
this time (e.g. in a `development` branch).  One exception is if the code
has already been merged to the release branch but additional finalizations
are found needed.


#### 3.1.1 Review issues

TODO


#### 3.1.2 Update HISTORY file

TODO


#### 3.1.3 Double-check the `sdist`

TODO

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


#### 3.1.4. Bump version number

TODO

For versioning your project, you may want to consider semantic versioning:
http://semver.org.


#### 3.1.5. Update `long_description` file

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


#### 3.1.6. Make sure tests pass

TODO


### 3.2. Merge to release branch

TODO:

* Discuss master/development
* Okay to make changes after this
* May want to wait a bit before next step


### 3.3 Register version on PyPI

After the repository is ready,
[register](http://docs.python.org/distutils/packageindex.html) the version
on PyPI.

Registering on PyPI adds an entry to PyPI for the version without uploading
any code.  Registering creates a page and URL for the version
(e.g. [http://pypi.python.org/pypi/Pizza/0.1.0](http://pypi.python.org/pypi/Pizza/0.1.0)),
stores metadata about the version, and adds the current "long_description"
to the version's page after converting it to HTML.  To register:

    $ python setup.py register

To test registering a version, you can use the `--repository/-r` option
to target the test PyPI server:

    $ python setup.py register -r test

where the string "test" corresponds to the "[test]" section of the `.pypirc`
file described above.  As a convenience, Pizza's `setup.py` has extra code
to prompt you for confirmation prior to registering or uploading:

    Are you sure you want to register to http://pypi.python.org/pypi (yes/no)?
    pizza: setup.py: [ERROR] aborted command: register

This lets you double-check what server you're interacting with and helps
prevent unintentional writes to PyPI.

Each time you create a new version for release, you should register that
version.  If you make a mistake or find that the metadata is not correct
after registering, it is okay to correct the source code and register again.
Subsequent registrations will overwrite the metadata previously stored for
that version.


#### Registration troubleshooting

If the long description shows up on PyPI as plain-text rather than HTML,
then the conversion to HTML failed.  See the `long_description` section
above for advice on troubleshooting conversion to HTML.  Also see
the bug report for PyPI
[bug #3539253](https://sourceforge.net/tracker/?func=detail&aid=3539253&group_id=66150&atid=513503).

If you get an error like the following after registering:

    Upload failed (401): You must be identified to edit package information

then there may be a problem with your `.pypirc` file.  Review the `.pypirc`
section above for possible issues.


### 3.4. Upload version to PyPI

After registering the version on PyPI,
[upload](http://docs.python.org/distutils/packageindex.html) the package
to PyPI:

    $ python setup.py sdist upload

This generates a `*.tar.gz` file by running `python setup.py sdist` and
then uploads the resulting file to the corresponding version on PyPI.
See prior sections of this document for more information on sdists.

You can use the `--repository/-r` option with the upload command just like
you can with register.  The project's upload command also prompts for
confirmation with the PyPI server name just like with register.

Unlike with the register command, PyPI does not let you "correct" an upload
after uploading.  You need to go through the process of creating a new
version, which means repeating the steps above as necessary.


### 3.5. Tag the commit

After
Here is a cheat-sheet for creating tags with Git.  List current tags:

    $ git tag -l -n3

Create an annotated tag:

    $ git tag -a -m "version description" "0.1.0"

Push a tag to GitHub:

    $ git push --tags <repository> 0.1.0
