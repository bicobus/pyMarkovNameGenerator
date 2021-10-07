# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2021 bicobus <bicobus@keemail.me>
import random
from functools import lru_cache


@lru_cache
def construct_alphabet(data: tuple) -> set:
    """
    Returns a set of the characters present in a list of words.

    Args:
        data (tuple): The list of words, in as a tuple.
    """
    alphabet = set()
    for word in data:
        alphabet |= set(word)
    return alphabet


def train(data: list, order: int):
    """
    Train the model on given data.

    Args:
        data (list): Training data, as a list of words.
        order (int): Order from the model in use.
    """
    bucket = {}
    while data:
        word = data.pop()
        word = "#" * order + word + "#"
        for i in range(len(word) - order):
            key = word[i:i + order]
            bucket.setdefault(key, [])
            try:
                bucket[key].append(word[i + order])
            except IndexError:  # XXX: exception shouldn't happen anyhow
                pass
    return bucket


def select_idx_from(chain):
    """Return a randomly selected index from the Markov Chain `chain`."""
    acc = 0
    totals = []
    for weight in chain:
        acc += weight
        totals.append(acc)

    rn = random.random() * acc
    for i, value in enumerate(totals):
        if rn < value:
            return i
    return 0


class Model:
    def __init__(self, data, order, prior):
        """
        Creates a new Markov model.

        Args:
            data (list): Training data for the model, as a list of words.
            order (int): The order the model will use. Models of order `n` will look
                back `n` characters within their context when determining the next
                letter.
            prior (float): The dirichlet prior, an additing smoothing "randomness"
                factor. Must be a float between 0 and 1.
        """
        if not data:
            raise ValueError("Dataset isn't valid: data is empty.")
        if not 0 <= prior <= 1:
            raise ValueError(
                "The prior dirichlet must be between 0 and 1, '{}' given.".format(prior)
            )
        self.chains = {}
        self.order = order
        self.prior = prior
        self.alphabet = sorted(list(construct_alphabet(tuple(data))))
        self.alphabet.insert(0, "#")

        self._cache = train(data, order)

        self.build_chains()

    def generate(self, key: str) -> str:
        """
        Attempts to generate the next letter in the word given in the context.

        Args:
            key (str): The previous order letters in the word.

        Returns: string or None
        """
        chain = self.chains.get(key)
        if chain:
            return self.alphabet[select_idx_from(chain)]
        return None

    def build_chains(self):
        """
        Build the Markov chains for the model.
        """
        self.chains = {}

        for key in self._cache.keys():
            self.chains.setdefault(key, [])
            for letter in self.alphabet:
                self.chains[key].append(self.prior + self._cache[key].count(letter))


class Generator:
    def __init__(self, data: list, order: int, prior: float):
        if not isinstance(order, int) or order <= 0:
            raise ValueError(
                "The value of 'order' must be an interger greater or equal to 1. (was %s)",
                order
            )
        if not data:
            raise ValueError(
                "Training dataset cannot be empty. We're expecting a list."
            )
        self.order = order

        self.models = [
            Model(data.copy(), order - i, prior)
            for i in range(order)
        ]

    def generate(self):
        word = "#" * self.order
        letter = self.letter_from(word)
        while letter != "#":
            if letter:
                word += letter
            letter = self.letter_from(word)
        return word

    def letter_from(self, context):
        letter = ""
        ctx_len = len(context)
        for model in self.models:
            letter = model.generate(context[ctx_len - model.order:ctx_len])
            if letter:
                break
        return letter
