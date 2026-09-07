from fastapi import FastAPI

from routers.products import router as products_router
from routers.categories import router as categories_router
from routers.users import router as users_router
from routers.cart import router as cart_router
from routers.orders import router as orders_router
from routers.admin import router as admin_router

app = FastAPI()

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(users_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(admin_router)

