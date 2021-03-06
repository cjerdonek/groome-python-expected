Pizza
=====

<!-- All Markdown comments are in the form of HTML comments to simplify
converting Markdown to reST.  We strip comments of this form prior to
passing the file to pandoc because pandoc preserves HTML and PyPI
rejects reST long descriptions containing HTML. -->

<!-- We leave the leading brackets empty here.  Otherwise, unwanted caption
text shows up in the reST version converted by pandoc.  This image is served
from GitHub pages because that's what GitHub prefers. -->
![](http://cjerdonek.github.com/groome/images/python-pizza.jpeg "python eating pizza")

<!-- Travis CI recommends the following for build-status images in Markdown:
http://about.travis-ci.org/docs/user/status-images/ -->
[![Build Status](https://travis-ci.org/cjerdonek/groome-python-expected.png)](https://travis-ci.org/cjerdonek/groome-python-expected)

[Pizza](https://github.com/cjerdonek/groome-python-expected) is a sample
demonstration project of a [Python](http://www.python.org) command-line script.

Pizza is the project you get when you render the
[Groome](http://cjerdonek.github.com/groome) project template
[groome-python](https://github.com/cjerdonek/groome-python) with its
sample configuration file.  For testing purposes, this project also serves
as the "expected" value of that template.  See the
[groome-python](https://github.com/cjerdonek/groome-python) project page
for more information about this project.

A minimal sample usage looks like--

    $ pizza hello crazy world
    3

The project page and source code is on
[GitHub](https://github.com/cjerdonek/groome-python-expected), and releases
can be found on [PyPI](http://pypi.python.org/pypi/Pizza)
(the Python Package Index).

Feedback is welcome.  You can file bug reports and feature requests on the
[project tracker](https://github.com/cjerdonek/groome-python-expected/issues).

[This project and `groome-python` are still being worked on and are not
yet usable.]


Requirements
------------

Pizza supports the following Python versions:

* Python 2.7
* Python 3.2
* Python 3.3
* [PyPy](http://pypy.org/)

Pizza has no third-party dependencies.

Installing for Python 3 requires that
[Distribute](http://packages.python.org/distribute/) be installed and that
[pip](http://www.pip-installer.org/) use Distribute.


Install It
----------

    $ pip install pizza


Test it
-------

    $ pizza --run-tests


Try it
------

    $ pizza hello crazy world
    3

For command-line help--

    $ pizza --help


Contributing
------------

To contribute to or modify the Pizza code base, consult
[`docs/developing.md`](docs/developing.md).


Author
------

Pizza is authored by [Chris Jerdonek](https://github.com/cjerdonek).


Copyright
---------

Copyright (C) 2013 Chris Jerdonek.  All rights reserved.

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
