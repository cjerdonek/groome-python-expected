Maintaining Pizza
=================

This document contains guidance on maintaining and contributing to Pizza.
The project README also contains some of this information.

For instructions on installing or using the application, consult the README or
[project page](https://github.com/cjerdonek/groome-python-expected) instead.
For instructions on releasing the application to PyPI and on how to use
`setup.py`, consult the `releasing.md` file in the `docs` folder.

XXX: add instructions for previewing a Markdown file.

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

XXX: (what does [template] mean, by the way?) add Tox instructions
after checking whether they're present anywhere already.
