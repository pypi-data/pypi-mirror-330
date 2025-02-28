from sleamdge.util import emojize


class MockEmoticon:
    name = "steamthumbsup"


def test_emojize():
    assert emojize(MockEmoticon) == "👍"
