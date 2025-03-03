from pytemplate.main import say_hello


def test_hello():
    assert say_hello() == 'Hello!'
