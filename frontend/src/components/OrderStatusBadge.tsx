import type { Order } from '../types/api';

const LABELS: Record<Order['status'], string> = {
  PENDENTE: 'Pendente',
  PAGO: 'Pago',
  CANCELADO: 'Cancelado',
};

export function OrderStatusBadge({ status }: { status: Order['status'] }) {
  return <span className={`status-badge status-${status.toLowerCase()}`}>{LABELS[status]}</span>;
}