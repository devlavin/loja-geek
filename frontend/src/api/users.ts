import { api } from './client';
import type { User } from '../types/api';

interface UpdateUserPayload {
  email?: string;
  password?: string;
}

export async function updateUser(id: number, payload: UpdateUserPayload): Promise<User> {
  const { data } = await api.patch<User>(`/users/${id}`, payload);
  return data;
}

export async function deleteUser(id: number): Promise<void> {
  await api.delete(`/users/${id}`);
}