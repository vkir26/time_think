import pytest
import random


@pytest.fixture
def seed() -> None:
    random.seed(1)
