import { api } from './client';
import type { Order } from '../types/api';

export type CreateOrderData = {
  phone: string;
  delivery_type: "retirada" | "entrega";
  address: string | null;
  payment_method: "pix" | "cartao" | "dinheiro";
};

export async function createOrder(
  orderData: CreateOrderData
): Promise<Order> {
  const { data } = await api.post<Order>("/orders", orderData);
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