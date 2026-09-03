import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()

def criar_token(usuario_id: int):
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes = ACESS_TOKEN_EXPIRE_MINUTES
    )
    
    payload = {
        "sub": str(usuario_id),
        "exp": expiracao
    }
    
    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credenciais_invalidas = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado."
    )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise credenciais_invalidas

    except jwt.InvalidTokenError:
        raise credenciais_invalidas

    resultado = db.execute(
        select(Usuario).where(Usuario.id == int(usuario_id))
    )

    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise credenciais_invalidas

    return usuario

def get_current_admin(
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas para administradores."
        )
    return usuario