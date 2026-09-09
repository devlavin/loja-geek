import { api } from './client';
import type { Product } from '../types/api';

interface ListProductsParams {
  name?: string;
  category?: string;
  min_price?: number;
  max_price?: number;
  skip?: number;
  limit?: number;
}

export async function listProducts(params: ListProductsParams = {}): Promise<Product[]> {
  const { data } = await api.get<Product[]>('/products', { params });
  return data;
}

export async function getProduct(id: number): Promise<Product> {
  const { data } = await api.get<Product>(`/products/${id}`);
  return data;
}

export interface ProductInput {
  name: string;
  description?: string;
  price: number;
  stock: number;
  category_id: number;
  image_url?: string;
}

export async function createProduct(item: ProductInput): Promise<void> {
  await api.post('/products', [item]);
}

export interface ProductUpdateInput {
  name?: string;
  description?: string;
  price?: number;
  stock?: number;
  category_id?: number;
  image_url?: string;
}

export async function updateProduct(id: number, payload: ProductUpdateInput): Promise<Product> {
  const { data } = await api.patch<Product>(`/products/${id}`, payload);
  return data;
}

export async function updateProductStock(id: number, stock: number): Promise<Product> {
  const { data } = await api.patch<Product>(`/products/${id}/stock`, { stock });
  return data;
}

export async function deleteProduct(id: number): Promise<void> {
  await api.delete(`/products/${id}`);
}