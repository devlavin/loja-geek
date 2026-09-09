// src/pages/admin/AdminOrders.tsx
import { useEffect, useState } from 'react';
import { adminListOrders, adminUpdateOrderStatus } from '../../api/admin';
import type { AdminOrder } from '../../api/admin';
import { getApiErrorMessage } from '../../api/error';
import { formatPrice } from '../../utils/format';
import { OrderStatusBadge } from '../../components/OrderStatusBadge';
import type { Order } from '../../types/api';

const NEXT_STATUSES: Record<Order['status'], Order['status'][]> = {
  PENDENTE: ['PAGO', 'CANCELADO'],
  PAGO: ['ENVIADO', 'CANCELADO'],
  ENVIADO: ['ENTREGUE'],
  ENTREGUE: [],
  CANCELADO: [],
};

const STATUS_LABELS: Record<Order['status'], string> = {
  PENDENTE: 'Pendente', PAGO: 'Pago', ENVIADO: 'Enviado', ENTREGUE: 'Entregue', CANCELADO: 'Cancelado',
};

export function AdminOrders() {
  const [orders, setOrders] = useState<AdminOrder[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [error, setError] = useState('');

  function load() {
    adminListOrders()
      .then(setOrders)
      .catch((err) => setError(getApiErrorMessage(err, 'Não foi possível carregar os pedidos.')))
      .finally(() => setIsLoading(false));
  }

  useEffect(load, []);

  async function handleStatusChange(orderId: number, status: Order['status']) {
    setError('');
    setUpdatingId(orderId);
    try {
      await adminUpdateOrderStatus(orderId, status);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível atualizar o status.'));
    } finally {
      setUpdatingId(null);
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;
  if (orders.length === 0) return <p className="page-status">Nenhum pedido ainda.</p>;

  return (
    <div className="admin-page">
      <h1>Pedidos</h1>

      {error && <p className="auth-error">{error}</p>}

      <div className="admin-order-list">
        {orders.map((order) => (
          <div key={order.id} className="admin-order-row">
            <button
              className="admin-order-summary"
              onClick={() => setExpandedId(expandedId === order.id ? null : order.id)}
            >
              <span>Pedido #{order.id}</span>
              <span>usuário #{order.user_id}</span>
              <OrderStatusBadge status={order.status} />
              <span>{formatPrice(order.total)}</span>
            </button>

            {expandedId === order.id && (
              <div className="admin-order-details">
                {order.items.map((item) => (
                  <div key={item.product_id} className="order-item-row">
                    <span>{item.quantity}x {item.name}</span>
                    <span>{formatPrice(item.subtotal)}</span>
                  </div>
                ))}

                <div className="admin-status-actions">
                  {NEXT_STATUSES[order.status].length === 0 ? (
                    <span className="field-hint">Nenhuma transição disponível.</span>
                  ) : (
                    NEXT_STATUSES[order.status].map((nextStatus) => (
                      <button
                        key={nextStatus}
                        className="btn-primary"
                        onClick={() => handleStatusChange(order.id, nextStatus)}
                        disabled={updatingId === order.id}
                      >
                        Marcar como {STATUS_LABELS[nextStatus]}
                      </button>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}