export interface Product {
    id: number;
    name: string;
    price: string;
    description: string | null;
    stock: number;
    category_id: number;
    image_url: string | null;
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
  role: 'user' | 'admin';
}

export interface CartItem {
  product_id: number;
  name: string;
  image_url: string | null;
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
  status: 'PENDENTE' | 'PAGO' | 'ENVIADO' | 'ENTREGUE' | 'CANCELADO';
  items: OrderItem[];
  total: string;
}