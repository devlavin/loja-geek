import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listOrders } from '../api/orders';
import type { Order } from '../types/api';
import { formatPrice } from '../utils/format';
import { OrderStatusBadge } from '../components/OrderStatusBadge';

export function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;
    listOrders()
      .then((data) => { if (!ignore) setOrders(data); })
      .finally(() => { if (!ignore) setIsLoading(false); });
    return () => { ignore = true; };
  }, []);

  if (isLoading) return <p className="page-status">Carregando...</p>;
  if (orders.length === 0) return <p className="page-status">Você ainda não fez nenhum pedido.</p>;

  return (
    <div className="order-list-page">
      <h1>Meus pedidos</h1>
      <div className="order-list">
        {orders.map((order) => (
          <Link key={order.id} to={`/pedidos/${order.id}`} className="order-row">
            <span>Pedido #{order.id}</span>
            <OrderStatusBadge status={order.status} />
            <span>{formatPrice(order.total)}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}