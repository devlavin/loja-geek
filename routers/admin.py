from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Pedido, Usuario
from auth import get_current_admin
from schema import AtualizarStatusPedido


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/pedidos")
def listar_todos_pedidos(
    admin: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido)
        .order_by(Pedido.id.desc())
    )

    pedidos = resultado.scalars().all()

    resposta = []

    for pedido in pedidos:
        itens = []

        for item in pedido.itens:
            itens.append({
                "produto_id": item.produto_id,
                "nome": item.produto.name,
                "quantidade": item.quantidade,
                "preco": item.preco,
                "subtotal": item.preco * item.quantidade
            })

        resposta.append({
            "id": pedido.id,
            "usuario_id": pedido.usuario_id,
            "status": pedido.status,
            "itens": itens,
            "total": pedido.total
        })

    return resposta

@router.get("/pedidos/{pedido_id}")
def visualizar_pedido_admin(
    pedido_id: int,
    admin: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido).where(
            Pedido.id == pedido_id
        )
    )

    pedido = resultado.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    itens = []

    for item in pedido.itens:
        itens.append({
            "produto_id": item.produto_id,
            "nome": item.produto.name,
            "quantidade": item.quantidade,
            "preco": item.preco,
            "subtotal": item.preco * item.quantidade
        })

    return {
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "status": pedido.status,
        "itens": itens,
        "total": pedido.total
    }
    
@router.patch("/pedidos/{pedido_id}/status")
def atualizar_status_pedido(
    pedido_id: int,
    dados: AtualizarStatusPedido,
    admin: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido).where(
            Pedido.id == pedido_id
        )
    )

    pedido = resultado.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    status_validos = [
        "PENDENTE",
        "PAGO",
        "ENVIADO",
        "ENTREGUE",
        "CANCELADO"
    ]

    if dados.status not in status_validos:
        raise HTTPException(
            status_code=400,
            detail="Status inválido."
        )

    transicoes_validas = {
        "PENDENTE": ["PAGO", "CANCELADO"],
        "PAGO": ["ENVIADO", "CANCELADO"],
        "ENVIADO": ["ENTREGUE"],
        "ENTREGUE": [],
        "CANCELADO": []
    }

    if dados.status not in transicoes_validas[pedido.status]:
        
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível alterar o pedido de {pedido.status} para {dados.status}."
        )

    pedido.status = dados.status

    db.commit()
    db.refresh(pedido)

    return {
        "message": "Status atualizado com sucesso.",
        "pedido_id": pedido.id,
        "status": pedido.status
    }

@router.get("/usuarios")
def listar_usuarios(
    admin: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Usuario)
        .order_by(Usuario.id.desc())
    )

    usuarios = resultado.scalars().all()

    resposta = []

    for usuario in usuarios:
        resposta.append({
            "id": usuario.id,
            "name": usuario.name,
            "email": usuario.email,
            "role": usuario.role
        })

    return resposta

@router.get("/usuarios/{usuario_id}")
def visualizar_usuario_admin(
    usuario_id: int,
    admin: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Usuario).where(
            Usuario.id == usuario_id
        )
    )

    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "id": usuario.id,
        "name": usuario.name,
        "email": usuario.email,
        "role": usuario.role
    }
    
@router.patch("/usuarios/{usuario_id}/role")
def atualizar_role_usuario(
    usuario_id: int,
    role: str,
    admin: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Usuario).where(
            Usuario.id == usuario_id
        )
    )

    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    roles_validas = [
        "user",
        "admin"
    ]

    if role not in roles_validas:
        raise HTTPException(
            status_code=400,
            detail="Role inválida."
        )

    if usuario.id == admin.id and role != "admin":
        raise HTTPException(
            status_code=400,
            detail="Você não pode remover sua própria permissão de administrador."
        )
    
    usuario.role = role

    db.commit()
    db.refresh(usuario)

    return {
        "message": "Role atualizada com sucesso.",
        "usuario_id": usuario.id,
        "role": usuario.role
    }