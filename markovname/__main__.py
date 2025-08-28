#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2021 bicobus <bicobus@keemail.me>
import argparse
import json
import sys
from pathlib import Path
from typing import Union

from wcwidth import wcswidth

from . import Generator
from ._version import __version__

FILEPATH = Path(__file__).resolve().parent


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "data", metavar="DATA", type=Path, nargs="?",
        default=Path(FILEPATH, "data"),
        help=(
            "Path containing the data sets. If none are given, will try to use the "
            "files shipped with the software."
        )
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
        "-g", "--generate", metavar="KEY", action="append",
        help="Which dataset to use. If not specified, use a random available set "
        "instead. Can be used multiple times to combine datasets."
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s v" + __version__
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbose mode."
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


def load_data(key: str, filenames: dict[str, Path]) -> Union[list[str], None]:
    jsonfile = filenames.get(key)
    if not jsonfile:
        return None
    return json.load(jsonfile.open())


def pad(maxlength: int, value: str, buff: int =1, padding: str =" ") -> str:
    return padding * (buff + max(0, (maxlength - wcswidth(value))))


def justify(keys, values):
    template = "{} → {}"
    maxlength = max([wcswidth(key) for key in keys])
    for key, value in zip(keys, values):
        yield template.format(
            pad(maxlength, key, buff=2) + key,
            value,
        )


def explain(args):
    """Print various informations about the current settings and training dataset."""
    if not args.verbose:
        return
    kv = {
        "Training dataset": args.generate,
        "Order": str(args.order),
        "Prior": str(args.prior),
        "Words to generate": str(args.number),
    }
    maxlength = max([wcswidth(k) for k in kv.keys()])
    for k, v in kv.items():
        print(
            "{}: {}".format(
                k,
                pad(maxlength, k, 0) + v
            )
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

    if not datasets:
        print("No dataset found for given path '{}'.".format(args.data), file=sys.stderr)
        sys.exit(1)

    if args.list:
        print("List of usable files:")
        for item in justify(datasets.keys(), datasets.values()):
            print(item)
    else:
        if not args.generate:  # Because argparse cannot have conditional requirements.
            args.generate = [random.choice(list(datasets.keys()))]
        dataset = []
        for set_name in args.generate:
            data = load_data(set_name, datasets)
            if not data:
                raise Exception(
                    (
                        "The training data selected '{}' couldn't be loaded. "
                        "Make sure you are selecting from the index (--list)."
                    ).format(set_name)
                )
            dataset.extend(data)
        generator = Generator(dataset, order=args.order, prior=args.prior)
        explain(args)
        i = 0
        tryagain = 0
        while i < args.number:
            result = generator.generate().strip("#")
            if result in dataset and tryagain < 3:
                tryagain += 1
                continue
            i += 1
            tryagain = 0
            print(result)


if __name__ == '__main__':
    main()
