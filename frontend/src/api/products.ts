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