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

<!-- TODO: change the following link to this:
  [![Build Status](https://travis-ci.org/cjerdonek/groome-python-expected.png)](https://travis-ci.org/cjerdonek/groome-python-expected)
once the resolution for the following pandoc issue is released:
  https://github.com/jgm/pandoc/issues/697 -->
![](https://travis-ci.org/cjerdonek/groome-python-expected.png "Build Status")

This is the working skeleton project you get when you render the
[Groome](http://cjerdonek.github.com/groome) template
[groome-python](https://github.com/cjerdonek/groome-python) with its
sample configuration file.

[This project and `groome-python` are still being worked on and are not
yet usable.]


Install It
----------

    TODO


Test it
-------

    TODO


Try it
------

    TODO


Hack it
-------

This section describes how to modify and contribute to Pizza.  In particular,
it shows you the way around and how to interact with Pizza from a source
checkout.

To run the main `pizza` script from source:

    $ python runpizza.py tomatoes garlic
    input: tomatoes, garlic

This script is essentially a development convenience for running:

    $ python -m pizza.scripts.pizza ...

which is in turn equivalent to the command above that
To get help and see all options:

    $ python runpizza.py --help

To run project tests (which are already stubbed out):

    $ python runpizza.py --run-tests


For Maintainers
---------------

For instructions on releasing Pizza and on how to use `setup.py`, consult
the `releasing.md` file in the `docs` folder of a source distribution.


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
