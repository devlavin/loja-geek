from fastapi import FastAPI

from routers.produtos import router as produtos_router
from routers.categorias import router as categorias_router
from routers.usuarios import router as usuarios_router
from routers.carrinho import router as carrinho_router
from routers.pedidos import router as pedidos_router

app = FastAPI()

app.include_router(produtos_router)
app.include_router(categorias_router)
app.include_router(usuarios_router)
app.include_router(carrinho_router)
app.include_router(pedidos_router)


