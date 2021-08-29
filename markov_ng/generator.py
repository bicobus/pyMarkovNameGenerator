# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2021 bicobus <bicobus@keemail.me>
import random


class Model:
    def __init__(self, data, order, prior, alphabet):
        """
        Creates a new Markov model.

        Args:
            data (list): Training data for the model, as a list of words.
            order (int): The order the model will use. Models of order `n` will look
                back `n` characters within their context when determining the next
                letter.
            prior (float): The dirichlet prior, an additing smoothing "randomness"
                factor. Must be a float between 0 and 1.
            alphabet (list):
        """
        if not alphabet or not data:
            raise ValueError("Dataset isn't valid. Either alphabet or data is empty.")
        if not 0 <= prior <= 1:
            raise ValueError(
                "The prior dirichlet must be between 0 and 1, '{}' given.".format(prior)
            )
        self.chains = {}
        self.order = order
        self.prior = prior
        self.alphabet = alphabet

        self._cache = {}

        self.train(data)
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
            return self.alphabet[self._select(chain)]
        return None

    def _select(self, chain):
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

    def train(self, data: list):
        """
        Train the model on given data.

        Args:
            data (list): Training data, as a list of words.
        """
        while data:
            d = data.pop()
            d = "#" * self.order + d + "#"
            for i in range(len(d) - self.order):
                key = d[i:i + self.order]
                self._cache.setdefault(key, [])
                try:
                    self._cache[key].append(d[i + self.order])
                except IndexError:  # XXX: exception shouldn't happen anyhow
                    pass

    def build_chains(self):
        """
        Build the Markov chains for the model.
        """
        self.chains = {}

        for key in self._cache.keys():
            for prediction in self.alphabet:  # XXX: find better terms
                self.chains.setdefault(key, [])
                self.chains[key].append(self.prior + self._cache[key].count(prediction))


class Generator:
    def __init__(self, data: list, order: int, prior: float):
        if not isinstance(order, int) or order <= 0:
            raise ValueError(
                "The value of 'order' must be an interger greater or equal to 1. (was %s)",
                order
            )
        self.order = order
        letters = set()
        for word in data:
            letters = letters.union({word[letter] for letter in range(len(word))})

        domain = list(letters)
        domain.insert(0, '#')
        self.models = [
            Model(data.copy(), order - i, prior, domain)
            for i in range(order)
        ]

    def generate(self):
        word = "#" * self.order
        letter = self.get_letter(word)
        while letter != "#":
            if letter:
                word += letter
            letter = self.get_letter(word)
        return word

    def get_letter(self, context):
        letter = ""
        context = context[len(context) - self.order:len(context)]
        for model in self.models:
            letter = model.generate(context)
            if not letter:
                order = model.order - 1
                context = context[len(context) - order:len(context)]
            else:
                break
        return letter
