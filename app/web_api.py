from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from app.core import get_task, Task
from app.session import ModeSelection, difficulty_parameters, SessionParameters
from app.messages import MenuMessage, RegisterMessage, AuthMessage, SessionMessage

from auth.config import AccountStorage, create_access_token, jwt_secret_key, ALGORITHM
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from jose import jwt, JWTError

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
    access_token: str
    token_type: str


SECURITY = HTTPBearer()


def get_current_user_id(creds: HTTPAuthorizationCredentials = Depends(SECURITY)) -> str:
    token = creds.credentials
    try:
        payload = jwt.decode(token=token, key=jwt_secret_key(), algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401)

        return str(user_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")


@router_v1.post("/signin")
def authorization(account: AuthAccount) -> AuthResponse:
    username = account.username
    password = account.password

    if username in AccountStorage().get_usernames():
        user_id: str | None = authenticate(username=username, password=password)
        if user_id:
            access_token = create_access_token(user_id=user_id)
            return AuthResponse(access_token=access_token, token_type="bearer")
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
    user_id: str = Depends(get_current_user_id), mode: SessionMode = Depends()
) -> SessionResponse:
    difficulty_level = difficulty_parameters[mode.difficulty]
    session = SessionData(question=get_task(), difficulty=difficulty_level)
    sessions[user_id] = session

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
    user_answer: SessionAnswer, user_id: str = Depends(get_current_user_id)
) -> dict[str, str | int] | AnswerResponse:
    session = sessions[user_id]
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
