from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Carrinho, ItemCarrinho, Produto, Usuario
from schema import CarrinhoResponse, ItemCarrinhoCreate
from auth import get_current_user


router = APIRouter(
    prefix="/carrinho",
    tags=["Carrinho"]
)


@router.get(
    "",
    response_model=CarrinhoResponse
)
def visualizar_carrinho(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Carrinho).where(
            Carrinho.usuario_id == usuario.id
        )
    )

    carrinho = resultado.scalar_one_or_none()

    if carrinho is None:
        carrinho = Carrinho(
            usuario_id=usuario.id
        )

        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

    itens = []

    for item in carrinho.itens:
        subtotal = item.produto.price * item.quantidade

        itens.append({
            "produto_id": item.produto.id,
            "nome": item.produto.name,
            "preco": item.produto.price,
            "quantidade": item.quantidade,
            "subtotal": subtotal
        })

    total = sum(item["subtotal"] for item in itens)

    return {
        "id": carrinho.id,
        "itens": itens,
        "total": total
    }
    
@router.post(
    "",
    response_model=CarrinhoResponse
)
def adicionar_ao_carrinho(
    item: ItemCarrinhoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Procura o carrinho do usuário
    resultado = db.execute(
        select(Carrinho).where(
            Carrinho.usuario_id == usuario.id
        )
    )

    carrinho = resultado.scalar_one_or_none()

    if carrinho is None:
        carrinho = Carrinho(
            usuario_id=usuario.id
        )

        db.add(carrinho)
        db.flush() #envia -> consigo o carrinho.id

    resultado = db.execute(
        select(Produto).where(
            Produto.id == item.produto_id
        )
    )

    produto = resultado.scalar_one_or_none()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    # Verifica estoque
    if item.quantidade > produto.estoque:
        raise HTTPException(
            status_code=400,
            detail="Quantidade solicitada maior que o estoque disponível."
        )

    # Verifica se o produto já está no carrinho
    resultado = db.execute(
        select(ItemCarrinho).where(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == item.produto_id
        )
    )

    item_existente = resultado.scalar_one_or_none()

    if item_existente is not None:
        raise HTTPException(
            status_code=400,
            detail="Produto já está no carrinho."
        )

    novo_item = ItemCarrinho(
        carrinho_id=carrinho.id,
        produto_id=item.produto_id,
        quantidade=item.quantidade,
        preco_adicionado=produto.price
    )

    db.add(novo_item)
    db.commit()
    db.refresh(carrinho)

    itens = []

    for item in carrinho.itens:
        subtotal = item.produto.price * item.quantidade

        itens.append({
            "produto_id": item.produto.id,
            "nome": item.produto.name,
            "preco": item.produto.price,
            "quantidade": item.quantidade,
            "subtotal": subtotal
        })

    total = sum(item["subtotal"] for item in itens)

    return {
        "id": carrinho.id,
        "itens": itens,
        "total": total
    }

@router.patch("/{produto_id}")
def alterar_quantidade(
    produto_id: int,
    quantidade: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A quantidade deve ser maior que zero."
        )

    resultado = db.execute(
        select(Carrinho).where(
            Carrinho.usuario_id == usuario.id
        )
    )

    carrinho = resultado.scalar_one_or_none()

    if carrinho is None:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado."
        )

    # Procura o produto no carrinho
    resultado = db.execute(
        select(ItemCarrinho).where(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == produto_id
        )
    )

    item = resultado.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não está no carrinho."
        )

    # Procura o produto para verificar o estoque
    resultado = db.execute(
        select(Produto).where(
            Produto.id == produto_id
        )
    )

    produto = resultado.scalar_one_or_none()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    if quantidade > produto.estoque:
        raise HTTPException(
            status_code=400,
            detail="Quantidade solicitada maior que o estoque disponível."
        )

    item.quantidade = quantidade

    db.commit()

    return {
        "message": "Quantidade atualizada com sucesso.",
        "produto_id": produto_id,
        "quantidade": quantidade
    }
    
@router.delete("/{produto_id}")
def remover_do_carrinho(
    produto_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    resultado = db.execute(
        select(Carrinho).where(
            Carrinho.usuario_id == usuario.id
        )
    )

    carrinho = resultado.scalar_one_or_none()

    if carrinho is None:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado."
        )

    resultado = db.execute(
        select(ItemCarrinho).where(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == produto_id
        )
    )

    item = resultado.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não está no carrinho."
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Produto removido do carrinho."
    }