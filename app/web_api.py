from fastapi import FastAPI
from messages import MenuMessage

app = FastAPI()


@app.get("/")
def greet() -> dict[str, str]:
    return {"message": "Добро пожаловать в игру `Время думать`"}


@app.get("/how_to_play")
def how_to_play() -> dict[str, MenuMessage]:
    return {"message": MenuMessage.HOW_TO_PLAY}
