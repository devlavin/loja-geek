import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../hooks/useCart";
import { updateCartItem, removeCartItem } from "../api/cart";
import { formatPrice } from "../utils/format";

export function Cart() {
  const navigate = useNavigate();
  const { cart, refreshCart } = useCart();
  const [pendingId, setPendingId] = useState<number | null>(null);

  async function handleQuantityChange(productId: number, newQuantity: number) {
    if (newQuantity <= 0) return;
    setPendingId(productId);
    try {
      await updateCartItem(productId, newQuantity);
      await refreshCart();
    } finally {
      setPendingId(null);
    }
  }

  async function handleRemove(productId: number) {
    setPendingId(productId);
    try {
      await removeCartItem(productId);
      await refreshCart();
    } finally {
      setPendingId(null);
    }
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="cart-page cart-empty">
        <p>Seu carrinho está vazio.</p>
        <Link to="/" className="btn-primary">
          Ver catálogo
        </Link>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <h1>Carrinho</h1>

      <div className="cart-list">
        {cart.items.map((item) => (
          <div key={item.product_id} className="cart-row">
            <div className="cart-row-thumb">
              {item.image_url && <img src={item.image_url} alt={item.name} />}
            </div>

            <div className="cart-row-info">
              <div className="cart-row-name">{item.name}</div>

              <div className="cart-row-price">
                {formatPrice(item.price)}
                {item.price_changed && (
                  <span className="price-changed-note">
                    preço mudou desde que você adicionou (era{" "}
                    {formatPrice(item.added_price)})
                  </span>
                )}
              </div>

              <div className="qty-row">
                <button
                  onClick={() =>
                    handleQuantityChange(item.product_id, item.quantity - 1)
                  }
                  disabled={pendingId === item.product_id || item.quantity <= 1}
                >
                  -
                </button>
                <span>{item.quantity}</span>
                <button
                  onClick={() =>
                    handleQuantityChange(item.product_id, item.quantity + 1)
                  }
                  disabled={pendingId === item.product_id}
                >
                  +
                </button>
              </div>
            </div>

            <div className="cart-row-subtotal">
              {formatPrice(item.subtotal)}
            </div>

            <button
              className="btn-link cart-remove"
              onClick={() => handleRemove(item.product_id)}
              disabled={pendingId === item.product_id}
            >
              remover
            </button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <div className="cart-total">
          <span>Total</span>
          <span>{formatPrice(cart.total)}</span>
        </div>
        <button className="btn-primary" onClick={() => navigate("/checkout")}>
          Finalizar pedido
        </button>
      </div>
    </div>
  );
}
