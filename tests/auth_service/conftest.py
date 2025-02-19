import pytest


@pytest.fixture
def user_data():
    return [
        # {"email": "example@email.ru", "password": "PASSWORD"},
        {"email": "example@email.com", "password": "PASSWORD"},
        {"email": "example@email.ya", "password": "PASSWORD"},
    ]


@pytest.fixture
def user_not_exists():
    return [
        {"email": "exist@email.ru", "password": "PASSWORD"},
        {"email": "exist@email.com", "password": "PASSWORD"},
        {"email": "exist@email.ya", "password": "PASSWORD"},
    ]


@pytest.fixture
def invalid_user_tokens():
    return [
        "12321",
        "aewlensdf,nsfdl",
    ]


@pytest.fixture
def invalid_user_data():
    return [
        {"email": "example", "password": "PASSWORD"},
        {"email": "", "password": "PASSWORD"},
        {"email": "exa", "password": ""},
        {"email": 4545, "password": 123},
        {"email": True, "password": 123},
    ]
