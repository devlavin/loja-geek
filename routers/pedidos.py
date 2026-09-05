from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Pedido, PedidoItem, Carrinho, Produto, Usuario
from schema import PedidoResponse
from auth import get_current_user

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@router.post(
    "",
    response_model=PedidoResponse
)
def criar_pedido(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        resultado = db.execute(
            select(Carrinho).where(
                Carrinho.usuario_id == usuario.id
            )
        )

        carrinho = resultado.scalar_one_or_none()

        if carrinho is None or not carrinho.itens:
            raise HTTPException(
                status_code=400,
                detail="Carrinho vazio."
            )

        total = 0
        itens_pedido = []

        for item in carrinho.itens:
            produto = item.produto

            if item.quantidade > produto.estoque:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para o produto: {produto.name}."
                )

            preco_atual = produto.price
            subtotal = preco_atual * item.quantidade

            total += subtotal

            itens_pedido.append({
                "produto": produto,
                "quantidade": item.quantidade,
                "preco": preco_atual
            })

        pedido = Pedido(
            usuario_id=usuario.id,
            status="PENDENTE",
            total=total
        )

        db.add(pedido)
        db.flush()

        for item in itens_pedido:
            produto = item["produto"]

            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                produto_id=produto.id,
                quantidade=item["quantidade"],
                preco=item["preco"]
            )

            db.add(pedido_item)

            produto.estoque -= item["quantidade"]

        for item in list(carrinho.itens):
            db.delete(item)

        db.commit()
        db.refresh(pedido)

        response_itens = []

        for item in pedido.itens:
            response_itens.append({
                "produto_id": item.produto_id,
                "nome": item.produto.name,
                "quantidade": item.quantidade,
                "preco": item.preco,
                "subtotal": item.preco * item.quantidade
            })

        return {
            "id": pedido.id,
            "status": pedido.status,
            "itens": response_itens,
            "total": pedido.total
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao criar pedido."
        )

@router.post("/{pedido_id}/pagar")
def pagar_pedido(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido).where(
            Pedido.id == pedido_id,
            Pedido.usuario_id == usuario.id
        )
    )

    pedido = resultado.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    if pedido.status != "PENDENTE":
        raise HTTPException(
            status_code=400,
            detail="Este pedido não pode ser pago."
        )

    # Pagamento simulado
    pedido.status = "PAGO"

    db.commit()
    db.refresh(pedido)

    return {
        "message": "Pagamento aprovado.",
        "pedido_id": pedido.id,
        "status": pedido.status
    }
    
@router.get(
    "",
    response_model=list[PedidoResponse]
)
def listar_pedidos(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido)
        .where(Pedido.usuario_id == usuario.id)
        .order_by(Pedido.id.desc())
    )

    pedidos = resultado.scalars().all()

    response = []

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

        response.append({
            "id": pedido.id,
            "status": pedido.status,
            "itens": itens,
            "total": pedido.total
        })

    return response

@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse
)
def visualizar_pedido(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido).where(
            Pedido.id == pedido_id,
            Pedido.usuario_id == usuario.id
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
        "status": pedido.status,
        "itens": itens,
        "total": pedido.total
    }
    
@router.patch("/{pedido_id}/cancelar")
def cancelar_pedido(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Pedido).where(
            Pedido.id == pedido_id,
            Pedido.usuario_id == usuario.id
        )
    )

    pedido = resultado.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    if pedido.status not in ["PENDENTE", "PAGO"]:
        raise HTTPException(
            status_code=400,
            detail="Este pedido não pode ser cancelado."
        )

    for item in pedido.itens:
        produto = item.produto

        produto.estoque += item.quantidade

    pedido.status = "CANCELADO"

    db.commit()
    db.refresh(pedido)

    return {
        "message": "Pedido cancelado com sucesso.",
        "pedido_id": pedido.id,
        "status": pedido.status
    }