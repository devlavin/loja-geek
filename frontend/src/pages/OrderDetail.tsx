import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getOrder, cancelOrder } from '../api/orders';
import { getApiErrorMessage } from '../api/error';
import type { Order } from '../types/api';
import { formatPrice } from '../utils/format';
import { OrderStatusBadge } from '../components/OrderStatusBadge';

export function OrderDetail() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCancelling, setIsCancelling] = useState(false);
  const [error, setError] = useState('');

  function loadOrder() {
    if (!id) return;
    getOrder(Number(id))
      .then(setOrder)
      .catch(() => setOrder(null))
      .finally(() => setIsLoading(false));
  }

  useEffect(loadOrder, [id]);

  async function handleCancel() {
    if (!order) return;
    setError('');
    setIsCancelling(true);
    try {
      await cancelOrder(order.id);
      loadOrder();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível cancelar o pedido.'));
    } finally {
      setIsCancelling(false);
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;
  if (!order) return <p className="page-status">Pedido não encontrado.</p>;

  const canCancel = order.status === 'PENDENTE' || order.status === 'PAGO';

  return (
    <div className="order-detail-page">
      <div className="order-detail-header">
        <h1>Pedido #{order.id}</h1>
        <OrderStatusBadge status={order.status} />
      </div>

      <div className="order-items">
        {order.items.map((item) => (
          <div key={item.product_id} className="order-item-row">
            <span>{item.quantity}x {item.name}</span>
            <span>{formatPrice(item.subtotal)}</span>
          </div>
        ))}
      </div>

      <div className="order-total">
        <span>Total</span>
        <span>{formatPrice(order.total)}</span>
      </div>

      {error && <p className="auth-error">{error}</p>}

      {canCancel && (
        <button className="btn-link" onClick={handleCancel} disabled={isCancelling}>
          {isCancelling ? 'Cancelando...' : 'Cancelar pedido'}
        </button>
      )}
    </div>
  );
}