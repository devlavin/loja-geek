from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Produto, Categoria
from schema import (
    Item,
    AtualizarPreco,
    AtualizarEstoque,
    ProdutoResponse,
    ProdutoComCategoriaResponse,
)

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

@router.post("")
def cadastrarProd(
    itens: list[Item],
    db: Session = Depends(get_db)
    ):
    try:
        
        for item in itens:
            
            resultado = db.execute(
            select(Categoria).where(Categoria.id == item.category_id)
            )

            categoria = resultado.scalar_one_or_none()

            if categoria is None:
                
                raise HTTPException(
                    status_code=404,
                    detail="Categoria não encontrada."
                )
        
            produto = Produto(
                name = item.name,
                price = item.price,
                estoque = item.estoque,
                category_id = item.category_id
            )
            db.add(produto)
    
        db.commit()

    except HTTPException:
        db.rollback()
        raise
    
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao cadastrar produto."
        )
    
    quantidade = len(itens)
    
    if quantidade == 1:
        return "Produto cadastrado com sucesso."
    
    return f"{quantidade} produtos cadastrados com sucesso."
    
@router.get(
    "",
    response_model=list[ProdutoResponse]
    )
def listar_produto(db: Session = Depends(get_db)):
    resultado = db.execute(select(Produto))
                           
    produtos = resultado.scalars().all()
    
    return produtos

@router.get("/{id}",
         response_model=ProdutoComCategoriaResponse
        )
def mostrarProd(id: int, db: Session = Depends(get_db)):

    resultado = db.execute(
        select(Produto).where(Produto.id == id)
    )
    produto = resultado.scalar_one_or_none()
    
    if produto is None:
        
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )
    return produto

@router.patch(
    "/{id}",
    response_model=ProdutoResponse
    )
def atualizarProd(id: int, item: AtualizarPreco, db: Session = Depends(get_db)):
    
    resultado = db.execute(
        select(Produto).where(Produto.id == id)
    )
    produto = resultado.scalar_one_or_none()
    
    if produto is None:
            
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )
    produto.price = item.price
    
    db.commit()
    
    return produto

@router.patch(
    "/{id}/estoque",
    response_model=ProdutoResponse
)
def atualizar_estoque(
    id: int,
    item: AtualizarEstoque,
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Produto).where(Produto.id == id)
    )

    produto = resultado.scalar_one_or_none()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    produto.estoque = item.estoque

    db.commit()

    return produto
    

@router.delete("/{id}")
def excluirProd(id: int, db: Session = Depends(get_db)):
    
    resultado = db.execute(
        select(Produto).where(Produto.id == id)
    )
    produto = resultado.scalar_one_or_none()
    
    if produto is None:
                
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )
    
    db.delete(produto)
    db.commit()
            
    return "Produto excluido com sucesso."