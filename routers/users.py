from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
import bcrypt
from auth import create_token, get_current_user
from models import User
from schema import UserCreate, UserLogin, UserResponse, UpdateUser


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado."
        )

    password_hash = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=password_hash,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(User).where(User.email == user.email)
    )

    user_db = result.scalar_one_or_none()

    if user_db is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou password inválidos."
        )

    password_valid = bcrypt.checkpw(
        user.password.encode("utf-8"),
        user_db.password_hash.encode("utf-8")
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Email ou password inválidos."
        )

    token = create_token(user_db.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    user: User = Depends(get_current_user)
):
    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    data: UpdateUser,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Você só pode editar seu próprio usuário."
        )

    if data.email is not None:
        result = db.execute(
            select(User).where(User.email == data.email)
        )

        existing_user = result.scalar_one_or_none()

        if existing_user is not None and existing_user.id != user.id:
            raise HTTPException(
                status_code=400,
                detail="E-mail já cadastrado."
            )

        user.email = data.email

    if data.password is not None:
        password_hash = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user.password_hash = password_hash

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Você só pode excluir seu próprio usuário."
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Usuário excluído com sucesso."
    }
