import { api } from './client';
import type { Order } from '../types/api';

export async function createOrder(): Promise<Order> {
  const { data } = await api.post<Order>('/orders');
  return data;
}

export async function listOrders(): Promise<Order[]> {
  const { data } = await api.get<Order[]>('/orders');
  return data;
}

export async function getOrder(id: number): Promise<Order> {
  const { data } = await api.get<Order>(`/orders/${id}`);
  return data;
}

// não devolvem o pedido completo — só confirmação
export async function payOrder(id: number): Promise<void> {
  await api.post(`/orders/${id}/pay`);
}

export async function cancelOrder(id: number): Promise<void> {
  await api.patch(`/orders/${id}/cancel`);
}