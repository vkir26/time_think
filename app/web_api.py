from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field

from app.core import get_task, Task
from app.session import ModeSelection, difficulty_parameters, SessionParameters
from auth.config import AccountStorage
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from app.messages import MenuMessage, RegisterMessage, AuthMessage

app = FastAPI()


@app.get("/")
def greet() -> dict[str, str]:
    return {"message": "Добро пожаловать в игру `Время думать`"}


router_v1 = APIRouter(prefix="/v1")


class RegisterAccount(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str | int = Field(min_length=5, max_length=15)


class RegisterAccountResponse(BaseModel):
    success_message: str


@router_v1.post("/signup")
def register_account(account: RegisterAccount) -> RegisterAccountResponse:
    username = account.username
    if name_is_exist(name=username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=RegisterMessage.NAME_EXISTS
        )

    password = account.password
    register(username=username, password=password)
    return RegisterAccountResponse(success_message=RegisterMessage.SUCCESS_REGISTER)


class AuthAccount(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str | int = Field(min_length=5, max_length=15)


class AuthResponse(BaseModel):
    message: str


@router_v1.post("/signin")
def authorization(account: AuthAccount) -> AuthResponse:
    username = account.username
    password = account.password

    if username in AccountStorage().get_usernames():
        if authenticate(username=username, password=password):
            return AuthResponse(message=AuthMessage.SUCCESS_AUTHORIZATION)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthMessage.INCORRECT_PASSWORD,
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=AuthMessage.USER_NOT_FOUND
        )


@router_v1.get("/how_to_play")
def how_to_play() -> dict[str, MenuMessage]:
    return {"message": MenuMessage.HOW_TO_PLAY}


class SessionMode(BaseModel):
    difficulty: ModeSelection = Field(default=ModeSelection.EASY)


class SessionData(BaseModel):
    question: Task = Field(default_factory=get_task)


class SessionResponse(BaseModel):
    question: str
    difficulty: SessionParameters


sessions: dict[str, SessionData] = {}


@router_v1.post("/start/{user}")
def start_session(user: str, mode: SessionMode = Depends()) -> SessionResponse:
    session = SessionData(question=get_task())

    sessions[user] = session

    return SessionResponse(
        question=session.question.task,
        difficulty=difficulty_parameters[mode.difficulty],
    )


class SessionAnswer(BaseModel):
    answer: int


@router_v1.post("/answer/{user}")
def answer(user: str, user_answer: SessionAnswer) -> bool:
    session = sessions[user]
    correct_answer = session.question.correct_answer

    return correct_answer.answer == user_answer.answer


app.include_router(router_v1)
