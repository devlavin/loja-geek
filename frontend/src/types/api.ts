export interface Product {
  id: number;
  name: string;
  price: string;      // Decimal do backend chega como string no JSON
  stock: number;
  category_id: number;
}

export interface ProductWithCategory extends Product {
  category: Category;
}

export interface Category {
  id: number;
  name: string;
}

export interface CategoryWithProducts extends Category {
  products: Product[];
}

export interface User {
  id: number;
  name: string;
  email: string;
}

export interface CartItem {
  product_id: number;
  name: string;
  price: string;
  added_price: string;
  price_changed: boolean;
  quantity: number;
  subtotal: string;
}

export interface Cart {
  id: number | null;
  items: CartItem[];
  total: string;
}

export interface OrderItem {
  product_id: number;
  name: string;
  quantity: number;
  price: string;
  subtotal: string;
}

export interface Order {
  id: number;
  status: 'PENDENTE' | 'PAGO' | 'CANCELADO';
  items: OrderItem[];
  total: string;
}