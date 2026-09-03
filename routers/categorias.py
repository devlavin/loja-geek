from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_admin
from models import Categoria, Usuario
from schema import (
    CategoriaCreate,
    AtualizarCategoria,
    CategoriaResponse,
    CategoriaComProdutosResponse
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

@router.post(
    "",
    response_model=CategoriaResponse
    )
def cadastrar_categoria(
    categoria: CategoriaCreate,
    _: Usuario = Depends(get_current_admin), 
    db: Session = Depends(get_db)
    ):
    
    nova_categoria = Categoria(
        name = categoria.name
    )
    
    db.add(nova_categoria)
    db.commit()
    
    return nova_categoria

@router.get(
    "",
    response_model=list[CategoriaResponse]
    )
def listar_categorias(db: Session = Depends(get_db)):
    resultado = db.execute(select(Categoria))
                           
    categorias = resultado.scalars().all()
    
    return categorias

@router.get("/{id}",
         response_model=CategoriaComProdutosResponse
        )
def mostrar_categorias(id: int, db: Session = Depends(get_db)):

    resultado = db.execute(
        select(Categoria).where(Categoria.id == id)
    )
    categoria = resultado.scalar_one_or_none()
    
    if categoria is None:
        
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )
    
    return categoria

@router.patch(
    "/{id}",
    response_model=CategoriaResponse
    )
def atualizar_categoria(
    id: int, 
    categoria_atualizada: AtualizarCategoria,
    _: Usuario = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Categoria).where(Categoria.id == id)
    )
    categoria = resultado.scalar_one_or_none()
    
    if categoria is None:
        
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )
    categoria.name = categoria_atualizada.name
    
    db.commit()
        
    return categoria

@router.delete("/{id}")
def excluir_categoria(
    id: int,
    _: Usuario = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Categoria).where(Categoria.id == id)
    )
    categoria = resultado.scalar_one_or_none()
    
    if categoria is None:
        
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )
    
    if categoria.produtos:
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir uma categoria que possui produtos."
        )
        
    db.delete(categoria)
    db.commit()
    
    return "Categoria excluida com sucesso."
        