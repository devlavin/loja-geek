from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
import bcrypt
from auth import criar_token, get_current_user
from models import Usuario
from schema import UsuarioCreate, UsuarioLogin, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.post(
    "",
    response_model=UsuarioResponse
)
def cadastrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Usuario).where(Usuario.email == usuario.email)
    )
    
    usuario_existente = resultado.scalar_one_or_none()
    
    if usuario_existente is not None:raise HTTPException(
        status_code=400,
        detail="E-mail já cadastrado."
    )
    
    senha_hash = bcrypt.hashpw(
        usuario.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
    
    novo_usuario = Usuario(
        name = usuario.name,
        email = usuario.email,
        password_hash = senha_hash
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario

@router.post("/login")
def login(
    usuario: UsuarioLogin,
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Usuario).where(Usuario.email == usuario.email)
    )

    usuario_db = resultado.scalar_one_or_none()

    if usuario_db is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )

    senha_valida = bcrypt.checkpw(
        usuario.password.encode("utf-8"),
        usuario_db.password_hash.encode("utf-8")
    )

    if not senha_valida:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )

    token = criar_token(usuario_db.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
@router.get("/me", response_model=UsuarioResponse)
def usuario_atual(
    usuario: Usuario = Depends(get_current_user)
):
    return usuario