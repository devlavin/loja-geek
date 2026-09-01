from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Produto

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

class AtualizarPreco(BaseModel):
    price: float
    
@app.post("/produtos")
def cadastrarProd(
    itens: list[Item],
    db: Session = Depends(get_db)
    ):
    
    for item in itens:
        produto = Produto(
            id = item.id,
            name = item.name,
            price = item.price
        )
        db.add(produto)
    
    db.commit()
    
    return "Produto cadastrado com sucesso."
    
@app.get("/produtos")
def listar_produto(db: Session = Depends(get_db)):
    resultado = db.execute(select(Produto))
                           
    produtos = resultado.scalars().all()
    
    return produtos

@app.get("/produtos/{id}")
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

@app.patch("/produtos/{id}")
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
    

@app.delete("/produtos/{id}")
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