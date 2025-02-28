import pytest
from src.auth_service.utils.pwd_helper import PWDHelper


@pytest.fixture
def pwd_helper() -> PWDHelper:
    return PWDHelper()

@pytest.fixture
def password() -> str:
    return "my_secure_password"

@pytest.fixture
def wrong_password() -> str:
    return "wrong_password"

class TestPWDHelper:
    def test_hash_password(self, pwd_helper: PWDHelper, password: str) -> None:
        hashed_password = pwd_helper.hash_password(password)

        assert hashed_password != password

        assert pwd_helper.verify_password(password, hashed_password)


    def test_verify_password_correct(self, pwd_helper: PWDHelper, password: str) -> None:
        hashed_password = pwd_helper.hash_password(password)

        assert pwd_helper.verify_password(password, hashed_password)


    def test_verify_password_incorrect(self, pwd_helper: PWDHelper, password: str, wrong_password: str) -> None:
        hashed_password = pwd_helper.hash_password(password)

        assert not pwd_helper.verify_password(wrong_password, hashed_password)


    def test_hash_password_different_salts(self, pwd_helper: PWDHelper, password: str) -> None:
        hashed_password1 = pwd_helper.hash_password(password)
        hashed_password2 = pwd_helper.hash_password(password)

        assert hashed_password1 != hashed_password2
