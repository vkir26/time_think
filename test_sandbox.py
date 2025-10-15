from pydantic import BaseModel


class Some(BaseModel):
    id: int


def test_some():
    model = Some(id=1)
    assert list(model.model_dump().values()) == [1]

    Some.model_validate(dict(id="13123"), strict=True)
