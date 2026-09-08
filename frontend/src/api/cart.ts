import { api } from './client';
import type { Cart } from '../types/api';

export async function getCart(): Promise<Cart> {
  const { data } = await api.get<Cart>('/cart');
  return data;
}

export async function addToCart(productId: number, quantity: number): Promise<Cart> {
  const { data } = await api.post<Cart>('/cart', { product_id: productId, quantity });
  return data;
}

// estes dois NÃO devolvem o carrinho — só uma mensagem de confirmação
export async function updateCartItem(productId: number, quantity: number): Promise<void> {
  await api.patch(`/cart/${productId}`, null, { params: { quantity } });
}

export async function removeCartItem(productId: number): Promise<void> {
  await api.delete(`/cart/${productId}`);
}