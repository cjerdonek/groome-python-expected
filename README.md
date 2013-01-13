Pizza
=====

<!-- All Markdown comments are in the format of one-line HTML comments -->
<!-- to simplify the conversion of Markdown to reST.  We strip comments -->
<!-- of this form prior to passing the file to pandoc because pandoc -->
<!-- preserves HTML and PyPI rejects reST long descriptions containing -->
<!-- HTML. -->

<!-- TODO: add a placeholder image. -->

<!-- TODO: check that this link renders nicely in both HTML and reST. -->
<!-- Also compare with the image markup used in the Molt project README. -->
[![Build Status](https://travis-ci.org/cjerdonek/groome-python-expected.png)](https://travis-ci.org/cjerdonek/groome-python-expected)

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


Hack on it
----------

This section describes how to use Pizza from a source checkout.  To run
the main `pizza` script from source:

    $ python runpizza.py tomatoes garlic
    input: tomatoes, garlic

This script is essentially a development convenience for running:

    $ python -m pizza.scripts.pizza ...

To get help and see all options:

    $ python runpizza.py --help

To run project tests (which are already stubbed out):

    $ python runpizza.py --run-tests


For Maintainers
---------------

See the module docstring of `setup.py` for instructions on preparing and
pushing new versions to PyPI.


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