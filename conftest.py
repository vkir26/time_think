import pytest
import random


@pytest.fixture
def seed():
    random.seed(1)
    return [random.randint(1, 7) for _ in range(2)]
