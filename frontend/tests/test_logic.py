import unittest

from unittest import mock
from unittest.mock import patch
from frontend.logic.game import hidden_word_handling, Game
from io import StringIO


class TestLogic(unittest.TestCase):
    def test_hidden_word_handling(self):
        word = "hello"
        cor_letters = "l"
        result = hidden_word_handling(word=word, cor_letters=cor_letters)
        expected = "__ll_"
        self.assertEqual(result, expected)

    def test_game_victory(self):
        word = "hello"
        cor_lett = "leo"
        incor_lett = "p"
        guess = "h"
        game = Game(word, cor_lett, incor_lett, guess)
        result = game.play()
        expected = {
            "hidden_word": "hello",
            "cor_lett": "leoh",
            "incor_lett": "p",
            "message": "Woo Hoo!",
            "victory": True,
            "game_over": True,
            "guess_status": 0,
        }
        self.assertEqual(result, expected)

    def test_game_defeat(self):
        word = "hello"
        cor_lett = "leo"
        incor_lett = "pqwyt"
        guess = "z"
        game = Game(word, cor_lett, incor_lett, guess)
        result = game.play()
        expected = {
            "hidden_word": "_ello",
            "cor_lett": "leo",
            "incor_lett": "pqwytz",
            "message": "bad luck!",
            "victory": False,
            "game_over": True,
            "guess_status": 0,
        }
        self.assertEqual(result, expected)
        
    