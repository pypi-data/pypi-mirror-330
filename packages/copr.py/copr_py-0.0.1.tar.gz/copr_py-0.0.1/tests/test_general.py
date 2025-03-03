from copr import *

def test_apiVersion():
  assert COPR.apiVersion()

def test_dataset():
  assert COPR.dataset()

def test_stats():
  assert isinstance(COPR.stats(), dict)
