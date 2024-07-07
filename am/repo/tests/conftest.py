# @pytest.fixture(scope="session")
# @pytest.fixture(scope="function")
# def test_pack():
# pass


# @pytest.fixture
# def test_pack(monkeypatch):
#     buffer = {"stdout": "", "write_calls": 0}

#     def fake_write(s):
#         buffer["stdout"] += s
#         buffer["write_calls"] += 1

#     monkeypatch.setattr(sys.stdout, "write", fake_write)
#     return buffer
