# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2021 bicobus <bicobus@keemail.me>
#
# flake8: noqa
import random
import json
from pathlib import Path

import pytest

from markov_ng.generator import Model, construct_alphabet, train, select_idx_from
from tests.fixtures import (
    ORDER,
    sample_data_list,
    sample_data_trained,
    sample_data_tuple,
    sample_data_chain,
)


def test_construct_alphabet(sample_data_tuple):
    letters = {"m", "a", "r", "k", "o", "v", "n", "e", "g", "t"}
    con = construct_alphabet(sample_data_tuple)
    assert con == letters


def test_train_type(sample_data_list):
    bucket = train(sample_data_list, ORDER)
    assert isinstance(bucket, dict)


def test_train_len(sample_data_list):
    bucket = train(sample_data_list, ORDER)
    assert len(bucket) == 20


def test_trained(sample_data_list, sample_data_trained):
    bucket = train(sample_data_list, ORDER)
    assert bucket == sample_data_trained


def test_build_chains(sample_data_list, sample_data_chain):
    mod = Model(sample_data_list, ORDER, 0)
    assert mod.chains == sample_data_chain


def generate(model):
    word = "#" * ORDER
    letter = letter_from(word, model)
    while letter != "#":
        if letter:
            word += letter
        letter = letter_from(word, model)
    return word

def letter_from(context, model):
    letter = ""
    ctx_len = len(context)
    letter = model.generate(context[ctx_len - model.order:ctx_len])
    return letter


@pytest.fixture
def load_jsondata():
    jsonfile = Path("tests/data/english_towns.json")
    if not jsonfile.exists():
        raise Exception("Test data files 'english_towns.json' isn't available.")
    return json.load(jsonfile.open())


def test_model(monkeypatch, load_jsondata):
    rnd = random.Random(123456789)
    def mock_random():
        return rnd.random()

    monkeypatch.setattr(random, "random", mock_random)

    test_model = Model(load_jsondata, ORDER, 0)
    word = generate(test_model)
    assert word == "###ormskirkby"
    word = generate(test_model)
    assert word == "###leobury"
    word = generate(test_model)
    assert word == "###ellenhalesham"
