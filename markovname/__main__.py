#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2021 bicobus <bicobus@keemail.me>
import argparse
import json
import sys
from pathlib import Path

from wcwidth import wcswidth

from ._version import __version__
from . import Generator


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "data", metavar="DATA", type=Path,
        help="Path containing the data sets."
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List the various dataset available to the software."
    )
    parser.add_argument(
        "-n", "--number", type=int, default=1,
        help="Amount of names to generate."
    )
    parser.add_argument(
        "-o", "--order", type=int, default=3,
        help="Highest order of model to use. Will use Katz's back-off model. It looks "
        "for the next letter based on the last \"n\" letters."
    )
    parser.add_argument(
        "-p", "--prior", type=float, default=0,
        help="The prior adds a constant probability that a random letter is picked "
        "from the alphabet when generating a new letter. Must be a number between 0 "
        "and 1."
    )
    parser.add_argument(
        "-g", "--generate", metavar="KEY", type=str,
        help="Which dataset to use. If not specified, use a random available set "
        "instead."
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s v" + __version__
    )


def available_dataset(path: Path):
    if not path.exists():
        raise ValueError(
            "The provided path '{}' doesn't exists.".format(path.resolve().as_uri())
        )
    if not path.is_dir():
        raise ValueError(
            "The provided path '{}' isn't a directory.".format(path.resolve().as_uri())
        )
    return {filename.name[:-5]: filename.resolve() for filename in path.glob("*.json")}


def load_data(key, filenames):
    jsonfile = filenames.get(key)
    if not jsonfile:
        return None
    return json.load(jsonfile.open())


def justify(keys, values):
    padding = " "
    template = "{} → {}"
    maxlength = max([wcswidth(key) for key in keys])
    for key, value in zip(keys, values):
        yield template.format(
            padding * (2 + max(0, (maxlength - wcswidth(key)))) + key,
            value,
        )


def main():
    import random

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_arguments(parser)
    args = parser.parse_args()

    try:
        datasets = available_dataset(args.data)
    except ValueError as e:
        print(f"ERROR: {e}\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.list:
        print("List of usable files:")
        for item in justify(datasets.keys(), datasets.values()):
            print(item)
    else:
        if not args.generate:  # Because argparse cannot have conditional requirements.
            args.generate = random.choice(list(datasets.keys()))
        generator = Generator(
            load_data(args.generate, datasets),
            order=args.order,
            prior=args.prior
        )
        for _ in range(args.number):
            print(generator.generate().strip('#'))


if __name__ == '__main__':
    main()
