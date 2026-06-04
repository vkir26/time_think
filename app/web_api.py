from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field

from app.core import get_task, Task
from app.session import ModeSelection, difficulty_parameters, SessionParameters
from auth.config import AccountStorage
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from app.messages import MenuMessage, RegisterMessage, AuthMessage, SessionMessage

app = FastAPI()


@app.get("/")
def greet() -> dict[str, str]:
    return {"message": "Добро пожаловать в игру `Время думать`"}


router_v1 = APIRouter(prefix="/v1")


class RegisterAccount(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str = Field(min_length=5, max_length=15)


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
    password: str = Field(min_length=5, max_length=15)


class AuthResponse(BaseModel):
    user_id: str


@router_v1.post("/signin")
def authorization(account: AuthAccount) -> AuthResponse:
    username = account.username
    password = account.password

    if username in AccountStorage().get_usernames():
        user_id: str | None = authenticate(username=username, password=password)
        if user_id:
            return AuthResponse(user_id=user_id)
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
    difficulty: SessionParameters

    correct_answers: int = 0
    wrong_answers: int = 0
    question_counter: int = 0


class SessionResponse(BaseModel):
    question: str
    difficulty: SessionParameters


sessions: dict[str, SessionData] = {}


@router_v1.post("/start")
def start_session(
    account: AuthResponse = Depends(authorization), mode: SessionMode = Depends()
) -> SessionResponse:
    difficulty_level = difficulty_parameters[mode.difficulty]
    session = SessionData(question=get_task(), difficulty=difficulty_level)
    sessions[account.user_id] = session

    return SessionResponse(
        question=session.question.task,
        difficulty=difficulty_level,
    )


class SessionAnswer(BaseModel):
    answer: int


class AnswerResponse(BaseModel):
    correct: bool
    correct_answers: int
    wrong_answers: int
    question: str


@router_v1.post("/answer")
def answer(
    user_answer: SessionAnswer, account: AuthResponse = Depends(authorization)
) -> dict[str, str | int] | AnswerResponse:
    session = sessions[account.user_id]
    correct_answer = session.question.correct_answer

    if session.question_counter >= session.difficulty.rounds:
        return {
            "message": SessionMessage.END_GAME,
            "correct": session.correct_answers,
            "wrong": session.wrong_answers,
        }
    if session.wrong_answers >= session.difficulty.lives:
        return {"message": "Закончились жизни"}

    correct = correct_answer.answer == user_answer.answer

    if correct:
        session.correct_answers += 1
        session.question = get_task()
    else:
        session.wrong_answers += 1

    session.question_counter += 1

    return AnswerResponse(
        correct=correct,
        correct_answers=session.correct_answers,
        wrong_answers=session.wrong_answers,
        question=session.question.task,
    )


app.include_router(router_v1)
