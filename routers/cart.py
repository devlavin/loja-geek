from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Cart, CartItem, Product, User
from schema import CartResponse, CartItemCreate
from auth import get_current_user


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)


@router.get(
    "",
    response_model=CartResponse
)
def get_cart(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Cart).where(
            Cart.user_id == user.id
        )
    )

    cart = result.scalar_one_or_none()

    if cart is None:
        new_cart = Cart(
            user_id=user.id
        )

        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)

        cart = new_cart

    items = []

    for item in cart.items:
        subtotal = item.product.price * item.quantity

        items.append({
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    total = sum(item["subtotal"] for item in items)

    return {
        "id": cart.id,
        "items": items,
        "total": total
    }


@router.post(
    "",
    response_model=CartResponse
)
def add_to_cart(
    item: CartItemCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Procura o carrinho do usuário
    result = db.execute(
        select(Cart).where(
            Cart.user_id == user.id
        )
    )

    cart = result.scalar_one_or_none()

    if cart is None:
        new_cart = Cart(
            user_id=user.id
        )

        db.add(new_cart)
        db.flush()  # envia para o banco e conseguimos o cart.id

        cart = new_cart

    result = db.execute(
        select(Product).where(
            Product.id == item.product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    # Verifica estoque
    if item.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="Quantidade solicitada maior que o estoque disponível."
        )

    # Verifica se o produto já está no carrinho
    result = db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item.product_id
        )
    )

    existing_item = result.scalar_one_or_none()

    if existing_item is not None:
        raise HTTPException(
            status_code=400,
            detail="Produto já está no carrinho."
        )

    new_item = CartItem(
        cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity,
        added_price=product.price
    )

    db.add(new_item)
    db.commit()
    db.refresh(cart)

    items = []

    for item in cart.items:
        subtotal = item.product.price * item.quantity

        items.append({
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    total = sum(item["subtotal"] for item in items)

    return {
        "id": cart.id,
        "items": items,
        "total": total
    }


@router.patch("/{product_id}")
def update_quantity(
    product_id: int,
    quantity: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="A quantidade deve ser maior que zero."
        )

    result = db.execute(
        select(Cart).where(
            Cart.user_id == user.id
        )
    )

    cart = result.scalar_one_or_none()

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado."
        )

    # Procura o produto no carrinho
    result = db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )

    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não está no carrinho."
        )

    # Procura o produto para verificar o estoque
    result = db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    if quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="Quantidade solicitada maior que o estoque disponível."
        )

    item.quantity = quantity

    db.commit()

    return {
        "message": "Quantidade atualizada com sucesso.",
        "product_id": product_id,
        "quantity": quantity
    }


@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Cart).where(
            Cart.user_id == user.id
        )
    )

    cart = result.scalar_one_or_none()

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado."
        )

    result = db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )

    item = result.scalar_one_or_none()

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
