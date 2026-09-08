import { api } from './client';
import type { LoginPayload, RegisterPayload, TokenResponse } from '../types/auth';
import type { User } from '../types/api';

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/users/login', payload);
  return data;
}

export async function register(payload: RegisterPayload): Promise<User> {
  const { data } = await api.post<User>('/users', payload);
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>('/users/me');
  return data;
}