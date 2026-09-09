import { NavLink, Outlet, Link } from 'react-router-dom';

export function AdminLayout() {
  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <Link to="/" className="admin-back">← Voltar à loja</Link>
        <nav className="admin-nav">
          <NavLink to="/admin/produtos" className={({ isActive }) => isActive ? 'active' : ''}>Produtos</NavLink>
          <NavLink to="/admin/categorias" className={({ isActive }) => isActive ? 'active' : ''}>Categorias</NavLink>
          <NavLink to="/admin/pedidos" className={({ isActive }) => isActive ? 'active' : ''}>Pedidos</NavLink>
          <NavLink to="/admin/usuarios" className={({ isActive }) => isActive ? 'active' : ''}>Usuários</NavLink>
        </nav>
      </aside>
      <main className="admin-content">
        <Outlet />
      </main>
    </div>
  );
}