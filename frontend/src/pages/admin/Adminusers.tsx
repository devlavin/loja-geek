// src/pages/admin/AdminUsers.tsx
import { useEffect, useState } from 'react';
import { adminListUsers, adminUpdateUserRole } from '../../api/admin';
import { getApiErrorMessage } from '../../api/error';
import { useAuth } from '../../hooks/useAuth';
import type { User } from '../../types/api';

export function AdminUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const { user: currentUser } = useAuth();

  function load() {
    adminListUsers()
      .then(setUsers)
      .catch((err) => setError(getApiErrorMessage(err, 'Não foi possível carregar os usuários.')))
      .finally(() => setIsLoading(false));
  }

  useEffect(load, []);

  async function handleToggleRole(u: User) {
    const newRole = u.role === 'admin' ? 'user' : 'admin';
    setError('');
    setUpdatingId(u.id);
    try {
      await adminUpdateUserRole(u.id, newRole);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível alterar a role.'));
    } finally {
      setUpdatingId(null);
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;

  return (
    <div className="admin-page">
      <h1>Usuários</h1>

      {error && <p className="auth-error">{error}</p>}

      <table className="admin-table">
        <thead><tr><th>Nome</th><th>E-mail</th><th>Role</th><th></th></tr></thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.name}</td>
              <td>{u.email}</td>
              <td>
                <span className={`status-badge ${u.role === 'admin' ? 'status-pago' : 'status-pendente'}`}>
                  {u.role === 'admin' ? 'Admin' : 'Cliente'}
                </span>
              </td>
              <td>
                <button
                  className="btn-link"
                  onClick={() => handleToggleRole(u)}
                  disabled={updatingId === u.id || u.id === currentUser?.id}
                  title={u.id === currentUser?.id ? 'Você não pode alterar sua própria role' : undefined}
                >
                  {u.role === 'admin' ? 'Remover admin' : 'Tornar admin'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}