from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Order, User
from auth import get_current_admin
from schema import UpdateStatusOrder


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/orders")
def list_orders(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order)
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
            "user_id": order.user_id,
            "status": order.status,
            "items": items,
            "total": order.total
        })

    return response


@router.get("/orders/{order_id}")
def get_order_admin(
    order_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order).where(
            Order.id == order_id
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
        "user_id": order.user_id,
        "status": order.status,
        "items": items,
        "total": order.total
    }


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    data: UpdateStatusOrder,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Order).where(
            Order.id == order_id
        )
    )

    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    valid_statuses = [
        "PENDENTE",
        "PAGO",
        "ENVIADO",
        "ENTREGUE",
        "CANCELADO"
    ]

    if data.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status inválido."
        )

    valid_transitions = {
        "PENDENTE": ["PAGO", "CANCELADO"],
        "PAGO": ["ENVIADO", "CANCELADO"],
        "ENVIADO": ["ENTREGUE"],
        "ENTREGUE": [],
        "CANCELADO": []
    }

    if data.status not in valid_transitions[order.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível alterar o pedido de {order.status} para {data.status}."
        )

    order.status = data.status

    db.commit()
    db.refresh(order)

    return {
        "message": "Status atualizado com sucesso.",
        "order_id": order.id,
        "status": order.status
    }


@router.get("/users")
def list_users(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(User)
        .order_by(User.id.desc())
    )

    users = result.scalars().all()

    response = []

    for user in users:
        response.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })

    return response


@router.get("/users/{user_id}")
def get_user_admin(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    valid_roles = [
        "user",
        "admin"
    ]

    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail="Role inválida."
        )

    if user.id == admin.id and role != "admin":
        raise HTTPException(
            status_code=400,
            detail="Você não pode remover sua própria permissão de administrador."
        )

    user.role = role

    db.commit()
    db.refresh(user)

    return {
        "message": "Role atualizada com sucesso.",
        "user_id": user.id,
        "role": user.role
    }
