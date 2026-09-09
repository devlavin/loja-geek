import { api } from './client';
import type { Order, User } from '../types/api';

export interface AdminOrder extends Order {
  user_id: number;
}

export async function adminListOrders(): Promise<AdminOrder[]> {
  const { data } = await api.get<AdminOrder[]>('/admin/orders');
  return data;
}

export async function adminUpdateOrderStatus(id: number, status: Order['status']): Promise<void> {
  await api.patch(`/admin/orders/${id}/status`, { status });
}

export async function adminListUsers(): Promise<User[]> {
  const { data } = await api.get<User[]>('/admin/users');
  return data;
}

export async function adminUpdateUserRole(id: number, role: 'user' | 'admin'): Promise<void> {
  await api.patch(`/admin/users/${id}/role`, { role });
}