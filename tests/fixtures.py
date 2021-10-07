# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2021 bicobus <bicobus@keemail.me>
import pytest

ORDER = 3  # default order is 3


@pytest.fixture
def sample_data_tuple():
    return (
        "markov",
        "name",
        "generator",
    )


@pytest.fixture
def sample_data_list(sample_data_tuple):
    return list(sample_data_tuple)


@pytest.fixture
def sample_data_trained():  # NOTE: valid for order=3
    return {
        "###": ["g", "n", "m"],
        "##g": ["e"],
        "#ge": ["n"],
        "gen": ["e"],
        "ene": ["r"],
        "ner": ["a"],
        "era": ["t"],
        "rat": ["o"],
        "ato": ["r"],
        "tor": ["#"],
        "##n": ["a"],
        "#na": ["m"],
        "nam": ["e"],
        "ame": ["#"],
        "##m": ["a"],
        "#ma": ["r"],
        "mar": ["k"],
        "ark": ["o"],
        "rko": ["v"],
        "kov": ["#"],
    }


@pytest.fixture
def sample_data_chain():  # NOTE: valid for order=3
    return {
        "###": [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        "##g": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        "#ge": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        "gen": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        "ene": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "ner": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "era": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        "rat": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "ato": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "tor": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "##n": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "#na": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "nam": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        "ame": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "##m": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "#ma": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "mar": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        "ark": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "rko": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        "kov": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
