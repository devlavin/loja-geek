import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useCart } from '../hooks/useCart';
import { UserMenu } from './UserMenu';

export function Navbar() {
  const { user } = useAuth();
  const { itemCount } = useCart();

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="logo-mark">
          <svg viewBox="0 0 32 32" width="26" height="26" fill="none">
            <path d="M16 6 L4 14 L14 15 L11 27 L16 18 L21 27 L18 15 L28 14 Z" fill="var(--brand)" />
          </svg>
          <span className="logo">Geek<span className="logo-accent">World</span></span>
        </Link>

        <div className="nav-links">
          <Link to="/">Catálogo</Link>
          <Link to="/carrinho" className="cart-pill">
            <span className="cart-dot" />
            Carrinho{itemCount > 0 ? ` · ${itemCount}` : ''}
          </Link>

          {user ? <UserMenu /> : <Link to="/login">Entrar</Link>}
        </div>
      </div>
    </nav>
  );
}