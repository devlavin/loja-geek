from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.admin import router as admin_router
from routers.cart import router as cart_router
from routers.categories import router as categories_router
from routers.orders import router as orders_router
from routers.products import router as products_router
from routers.users import router as users_router


app = FastAPI(
    title="Loja Geek API",
    description="API REST para gerenciamento de uma loja geek.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # onde o Vite roda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(cart_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(users_router)