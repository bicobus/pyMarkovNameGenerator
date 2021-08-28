=======================
 pyMarkovNameGenerator
=======================

Markov chain-based name generator based on `Sam Twidale`_ implementation in
Haxe.

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
                            Highest order of model to use. Will use Katz's
                            back-off model.  It looks for the next letter based
                            on the last "n" letters.  (default: 3)
      -p PRIOR, --prior PRIOR
                            The prior adds a constant probability that a
                            random letter is picked from the alphabet when
                            generating a new letter. Must be a number between 0
                            and 1. (default: 0)
      -g KEY, --generate KEY
                            Which dataset to use. Required unless --list is
                            passed as an argument. (default: None)
      -V, --version         show program's version number and exit



.. _Sam Twidale: https://github.com/Tw1ddle/MarkovNameGenerator
.. _wcwidth: https://github.com/jquast/wcwidth/
