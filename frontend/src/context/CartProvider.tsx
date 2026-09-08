import { useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import type { Cart } from '../types/api';
import { getCart } from '../api/cart';
import { useAuth } from '../hooks/useAuth';
import { CartContext } from './cart-context';

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<Cart | null>(null);
  const { user } = useAuth();

  const refreshCart = useCallback(async () => {
    if (!user) return;
    try {
      const data = await getCart();
      setCart(data);
    } catch {
      setCart(null);
    }
  }, [user]);

  useEffect(() => {
    if (!user) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- reset intencional ao deslogar
      setCart(null);
      return;
    }

    let ignore = false;

    getCart()
      .then((data) => {
        if (!ignore) setCart(data);
      })
      .catch(() => {
        if (!ignore) setCart(null);
      });

    return () => { ignore = true; };
  }, [user]);

  const itemCount = cart?.items.reduce((sum, item) => sum + item.quantity, 0) ?? 0;

  return (
    <CartContext.Provider value={{ cart, itemCount, refreshCart }}>
      {children}
    </CartContext.Provider>
  );
}