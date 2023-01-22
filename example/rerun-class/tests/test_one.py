class TestOne:
    count = 0

    def test_1a(self):
        assert True

    def test_1b(self):
        TestOne.count += 1
        assert TestOne.count == 2

    def test_1c(self):
        assert True
