.. image:: https://img.shields.io/pypi/pyversions/markovname   :alt: PyPI - Python Version

.. image:: https://github.com/bicobus/pyMarkovNameGenerator/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/bicobus/pyMarkovNameGenerator/actions/workflows/tests.yml

=======================
 pyMarkovNameGenerator
=======================

Markov chain-based name generator based on `Sam Twidale`_ implementation in
Haxe. consider this work to be a python port with functionnally the same level
of functionality. Feed it a list of training data, and it'll spew out a bunch of
new words.

It comes with the training data compiled by Sam, and made available under
Creative Commons `BY-NC 4.0`.

If you appreciate this work, consider `buying me a coffee`_.

Install using::

  pip install markovname

Requirements
============
This software has been developped and tested with python 3.9. Any earlier
version might not work.

A minor dependency on wcwidth_, make sure it is installed using ``pip``, your
package manager or whatever method you are familiar with. It is only necessary
if you plan to use the main module. If you're only interested in the generator,
then ``wcwidth`` can be ignored.

If you have poetry_ available, you can initialize a virtual environment with::

    poetry install

Usage
=====

The software reads sample data from json formatted datasets. See the data folder
of this repository for examples.

::

   usage: __main__.py [-h] [--list] [-n NUMBER] [-o ORDER] [-p PRIOR] [-g KEY] [-V] DATA

   positional arguments:
     DATA                  Path containing the data sets.

   optional arguments:
     -h, --help            show this help message and exit
     --list                List the various dataset available to the software.
                           (default: False)
     -n NUMBER, --number NUMBER
                           Amount of names to generate. (default: 1)
     -o ORDER, --order ORDER
                           Highest order of model to use. Will use Katz's back-
                           off model. It looks for the next letter based on the
                           last "n" letters. (default: 3)
     -p PRIOR, --prior PRIOR
                           The prior adds a constant probability that a random
                           letter is picked from the alphabet when generating a
                           new letter. Must be a number between 0 and 1.
                           (default: 0)
     -g KEY, --generate KEY
                           Which dataset to use. If not specified, use a random
                           available set instead. (default: None)
     -V, --version         show program's version number and exit



.. _Sam Twidale: https://github.com/Tw1ddle/MarkovNameGenerator
.. _wcwidth: https://github.com/jquast/wcwidth/
.. _poetry: https://python-poetry.org/
.. _Buy me a coffee: https://ko-fi.com/S6S36HZ6I
