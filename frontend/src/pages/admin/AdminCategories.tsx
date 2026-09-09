// src/pages/admin/AdminCategories.tsx
import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { listCategories, createCategory, updateCategory, deleteCategory } from '../../api/categories';
import { getApiErrorMessage } from '../../api/error';
import type { Category } from '../../types/api';

export function AdminCategories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const [newName, setNewName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState('');

  function load() {
    listCategories()
      .then(setCategories)
      .catch((err) => setError(getApiErrorMessage(err, 'Não foi possível carregar as categorias.')))
      .finally(() => setIsLoading(false));
  }

  useEffect(load, []);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      await createCategory(newName);
      setNewName('');
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível criar a categoria.'));
    } finally {
      setIsSubmitting(false);
    }
  }

  function startEdit(c: Category) {
    setEditingId(c.id);
    setEditValue(c.name);
  }

  async function saveEdit() {
    if (editingId === null) return;
    setError('');
    try {
      await updateCategory(editingId, editValue);
      setEditingId(null);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível salvar.'));
    }
  }

  async function handleDelete(id: number) {
    if (!confirm('Excluir esta categoria?')) return;
    setError('');
    try {
      await deleteCategory(id);
      load();
    } catch (err) {
      // se a categoria tiver produtos, a API já recusa com uma mensagem explicando
      setError(getApiErrorMessage(err, 'Não foi possível excluir a categoria.'));
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;

  return (
    <div className="admin-page">
      <h1>Categorias</h1>

      {error && <p className="auth-error">{error}</p>}

      <form onSubmit={handleCreate} className="admin-inline-form">
        <input type="text" placeholder="Nova categoria" value={newName} onChange={(e) => setNewName(e.target.value)} required />
        <button className="btn-primary" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Criando...' : 'Adicionar'}
        </button>
      </form>

      <table className="admin-table">
        <tbody>
          {categories.map((c) => (
            <tr key={c.id}>
              <td>
                {editingId === c.id ? (
                  <span className="admin-edit-cell">
                    <input value={editValue} onChange={(e) => setEditValue(e.target.value)} autoFocus />
                    <button onClick={saveEdit}>salvar</button>
                    <button onClick={() => setEditingId(null)}>cancelar</button>
                  </span>
                ) : (
                  c.name
                )}
              </td>
              <td>
                {editingId !== c.id && (
                  <>
                    <button className="btn-link" onClick={() => startEdit(c)}>editar</button>
                    <button className="btn-link danger" onClick={() => handleDelete(c.id)}>excluir</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}