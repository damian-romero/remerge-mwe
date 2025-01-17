# flake8: noqa
from src.remerge import __version__
from src.remerge import run
from src.remerge.core import Lexeme, SelectionMethod

from .fixtures import sample_corpus


def test_version():
    assert __version__ == "0.1.1"


def test_single_iter(sample_corpus):
    winners = run(sample_corpus, 1)
    assert winners[0].merged_lexeme == Lexeme(("you", "know"), 0)


def test_consecutive_single():
    """The point of this test is to make sure that the greedy bigram merge is occuring correctly
    and the algorithm does not try to merge the middle bigram here."""
    corpus = ["a a a a".split()]
    winners = run(corpus, 2)
    assert winners[0].merge_token_count == 2  # count == 3 is incorrect
    assert winners[1].merged_lexeme == Lexeme(("a", "a", "a", "a"), 0)


def test_consecutive_remainder():
    """The point of this test is to make sure that the greedy bigram merge is occuring correctly
    and the algorithm does not try to merge the trailing bigram"""
    corpus = ["c a b a b a b d".split()]
    winners = run(corpus, 2, method=SelectionMethod.frequency)
    assert winners[0].merge_token_count == 3
    assert winners[1].merge_token_count == 1
