from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Order, OrderItem, Cart, Product, User
from schema import OrderResponse
from auth import get_current_user


router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post(
    "",
    response_model=OrderResponse
)
def create_order(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            select(Cart).where(
                Cart.user_id == user.id
            )
        )

        cart = result.scalar_one_or_none()

        if cart is None or not cart.items:
            raise HTTPException(
                status_code=400,
                detail="Carrinho vazio."
            )

        total = 0
        order_items = []

        for item in cart.items:
            product = item.product

            if item.quantity > product.stock:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para o produto: {product.name}."
                )

            current_price = product.price
            subtotal = current_price * item.quantity

            total += subtotal

            order_items.append({
                "product": product,
                "quantity": item.quantity,
                "price": current_price
            })

        new_order = Order(
            user_id=user.id,
            status="PENDENTE",
            total=total
        )

        db.add(new_order)
        db.flush()

        for item in order_items:
            product = item["product"]

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item["quantity"],
                price=item["price"]
            )

            db.add(order_item)

            product.stock -= item["quantity"]

        for item in list(cart.items):
            db.delete(item)

        db.commit()
        db.refresh(new_order)

        response_items = []

        for item in new_order.items:
            response_items.append({
                "product_id": item.product_id,
                "name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.price * item.quantity
            })

        return {
            "id": new_order.id,
            "status": new_order.status,
            "items": response_items,
            "total": new_order.total
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


@router.post("/{order_id}/pay")
def pay_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == user.id
        )
    )

    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    if order.status != "PENDENTE":
        raise HTTPException(
            status_code=400,
            detail="Este pedido não pode ser pago."
        )

    # Pagamento simulado
    order.status = "PAGO"

    db.commit()
    db.refresh(order)

    return {
        "message": "Pagamento aprovado.",
        "order_id": order.id,
        "status": order.status
    }


@router.get(
    "",
    response_model=list[OrderResponse]
)
def list_orders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.id.desc())
    )

    orders = result.scalars().all()

    response = []

    for order in orders:
        items = []

        for item in order.items:
            items.append({
                "product_id": item.product_id,
                "name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.price * item.quantity
            })

        response.append({
            "id": order.id,
            "status": order.status,
            "items": items,
            "total": order.total
        })

    return response


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == user.id
        )
    )

    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    items = []

    for item in order.items:
        items.append({
            "product_id": item.product_id,
            "name": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
            "subtotal": item.price * item.quantity
        })

    return {
        "id": order.id,
        "status": order.status,
        "items": items,
        "total": order.total
    }


@router.patch("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == user.id
        )
    )

    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    if order.status not in ["PENDENTE", "PAGO"]:
        raise HTTPException(
            status_code=400,
            detail="Este pedido não pode ser cancelado."
        )

    for item in order.items:
        product = item.product

        product.stock += item.quantity

    order.status = "CANCELADO"

    db.commit()
    db.refresh(order)

    return {
        "message": "Pedido cancelado com sucesso.",
        "order_id": order.id,
        "status": order.status
    }
