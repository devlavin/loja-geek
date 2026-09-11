// src/pages/Checkout.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../hooks/useCart";
import { useAuth } from "../hooks/useAuth";
import { createOrder, payOrder } from "../api/orders";
import { getApiErrorMessage } from "../api/error";
import { formatPrice } from "../utils/format";

export function Checkout() {
  const { cart, refreshCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [phone, setPhone] = useState("");
  const [deliveryType, setDeliveryType] = useState<"retirada" | "entrega">(
    "retirada",
  );
  const [address, setAddress] = useState("");
  const [paymentMethod, setPaymentMethod] = useState<
    "pix" | "cartao" | "dinheiro"
  >("pix");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  if (!cart || cart.items.length === 0) {
    return <p className="page-status">Seu carrinho está vazio.</p>;
  }

async function handleConfirm() {
  setError('');
  setIsSubmitting(true);

  try {
    const order = await createOrder({
      phone,
      delivery_type: deliveryType,
      address: deliveryType === 'entrega' ? address : undefined,
      payment_method: paymentMethod,
    });
    await payOrder(order.id);
    await refreshCart();
    navigate(`/pedidos/${order.id}`);
  } catch (err) {
    setError(getApiErrorMessage(err, 'Não foi possível concluir o pedido.'));
  } finally {
    setIsSubmitting(false);
  }
}

  return (
    <div className="checkout-page">
      <h1>Finalizar pedido</h1>

      <div className="checkout-summary">
        {cart.items.map((item) => (
          <div key={item.product_id} className="checkout-item">
            <span>
              {item.quantity}x {item.name}
            </span>
            <span>{formatPrice(item.subtotal)}</span>
          </div>
        ))}
        <div className="checkout-total">
          <span>Total</span>
          <span>{formatPrice(cart.total)}</span>
        </div>
      </div>

      <div className="checkout-form">
        <div className="form-group">
          <label>Nome</label>
          <input type="text" value={user?.name ?? ""} disabled />
          <label>Telefone</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="(xx)xxxxx-xxxx"
          />
        </div>

        <div className="form-group">
          <label>Como você quer receber?</label>
          <div className="radio-row">
            <label>
              <input
                type="radio"
                checked={deliveryType === "retirada"}
                onChange={() => setDeliveryType("retirada")}
              />
              Retirar na loja
            </label>
            <label>
              <input
                type="radio"
                checked={deliveryType === "entrega"}
                onChange={() => setDeliveryType("entrega")}
              />
              Entrega
            </label>
          </div>
        </div>

        {deliveryType === "entrega" && (
          <div className="form-group">
            <label>Endereço</label>
            <input
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="Rua, número, bairro"
            />
          </div>
        )}

        <div className="form-group">
          <label>Forma de pagamento</label>
          <div className="radio-row">
            <label>
              <input
                type="radio"
                checked={paymentMethod === "pix"}
                onChange={() => setPaymentMethod("pix")}
              />
              Pix
            </label>
            <label>
              <input
                type="radio"
                checked={paymentMethod === "cartao"}
                onChange={() => setPaymentMethod("cartao")}
              />
              Cartão
            </label>
            <label>
              <input
                type="radio"
                checked={paymentMethod === "dinheiro"}
                onChange={() => setPaymentMethod("dinheiro")}
              />
              Dinheiro
            </label>
          </div>
        </div>
      </div>

      {error && <p className="auth-error">{error}</p>}

      <button
        className="btn-primary"
        onClick={handleConfirm}
        disabled={isSubmitting}
      >
        {isSubmitting ? "Confirmando..." : "Confirmar pedido"}
      </button>
    </div>
  );
}
