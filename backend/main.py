from fastapi import FastAPI, Request

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from limiter import limiter
from fastapi.middleware.cors import CORSMiddleware
import os

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

origins = [
    "https://loja-geek-phi.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.include_router(admin_router)
app.include_router(cart_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(users_router)
