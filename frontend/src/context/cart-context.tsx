import { createContext } from 'react';
import type { Cart } from '../types/api';

export interface CartContextValue {
  cart: Cart | null;
  itemCount: number;
  refreshCart: () => Promise<void>;
}

export const CartContext = createContext<CartContextValue | undefined>(undefined);