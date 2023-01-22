import pytest


class TestOne:
    @pytest.mark.dependency(name="test_1", scope="class")
    def test_1(self):
        assert True

    @pytest.mark.dependency(name="test_2", depends=["test_1"],  scope="class")
    def test_2(self):
        assert False

    @pytest.mark.dependency(name="test_3", depends=["test_2"], scope="class")
    def test_3(self):
        assert True
