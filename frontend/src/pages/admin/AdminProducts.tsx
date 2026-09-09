// src/pages/admin/AdminProducts.tsx
import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { listProducts, createProduct, updateProductPrice, updateProductStock, deleteProduct } from '../../api/products';
import { listCategories } from '../../api/categories';
import { getApiErrorMessage } from '../../api/error';
import type { Product, Category } from '../../types/api';
import { formatPrice } from '../../utils/format';

export function AdminProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const [isCreating, setIsCreating] = useState(false);
  const [newName, setNewName] = useState('');
  const [newPrice, setNewPrice] = useState('');
  const [newStock, setNewStock] = useState('');
  const [newCategoryId, setNewCategoryId] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [editing, setEditing] = useState<{ id: number; field: 'price' | 'stock' } | null>(null);
  const [editValue, setEditValue] = useState('');

  function categoryName(id: number) {
    return categories.find((c) => c.id === id)?.name ?? '—';
  }

  function load() {
    Promise.all([listProducts(), listCategories()])
      .then(([p, c]) => {
        setProducts(p);
        setCategories(c);
      })
      .catch((err) => setError(getApiErrorMessage(err, 'Não foi possível carregar os produtos.')))
      .finally(() => setIsLoading(false));
  }

  useEffect(load, []);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await createProduct({
        name: newName,
        price: Number(newPrice),
        stock: Number(newStock),
        category_id: Number(newCategoryId),
      });
      setNewName('');
      setNewPrice('');
      setNewStock('');
      setNewCategoryId('');
      setIsCreating(false);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível criar o produto.'));
    } finally {
      setIsSubmitting(false);
    }
  }

  function startEdit(id: number, field: 'price' | 'stock', currentValue: string) {
    setEditing({ id, field });
    setEditValue(currentValue);
  }

  async function saveEdit() {
    if (!editing) return;
    setError('');

    try {
      if (editing.field === 'price') {
        await updateProductPrice(editing.id, Number(editValue));
      } else {
        await updateProductStock(editing.id, Number(editValue));
      }
      setEditing(null);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível salvar.'));
    }
  }

  async function handleDelete(id: number) {
    if (!confirm('Excluir este produto?')) return;
    setError('');
    try {
      await deleteProduct(id);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, 'Não foi possível excluir o produto.'));
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <h1>Produtos</h1>
        <button className="btn-primary" onClick={() => setIsCreating((v) => !v)}>
          {isCreating ? 'Cancelar' : 'Novo produto'}
        </button>
      </div>

      {error && <p className="auth-error">{error}</p>}

      {isCreating && (
        <form onSubmit={handleCreate} className="admin-inline-form">
          <input type="text" placeholder="Nome do produto" value={newName} onChange={(e) => setNewName(e.target.value)} required />
          <input type="number" step="0.01" min="0.01" placeholder="Preço" value={newPrice} onChange={(e) => setNewPrice(e.target.value)} required />
          <input type="number" min="0" placeholder="Estoque" value={newStock} onChange={(e) => setNewStock(e.target.value)} required />
          <select value={newCategoryId} onChange={(e) => setNewCategoryId(e.target.value)} required>
            <option value="">Categoria</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
          <button className="btn-primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Criando...' : 'Criar'}
          </button>
        </form>
      )}

      <table className="admin-table">
        <thead>
          <tr><th>Nome</th><th>Categoria</th><th>Preço</th><th>Estoque</th><th></th></tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.name}</td>
              <td>{categoryName(p.category_id)}</td>
              <td>
                {editing?.id === p.id && editing.field === 'price' ? (
                  <span className="admin-edit-cell">
                    <input type="number" step="0.01" min="0.01" value={editValue} onChange={(e) => setEditValue(e.target.value)} autoFocus />
                    <button onClick={saveEdit}>salvar</button>
                    <button onClick={() => setEditing(null)}>cancelar</button>
                  </span>
                ) : (
                  <button className="btn-link" onClick={() => startEdit(p.id, 'price', p.price)}>
                    {formatPrice(p.price)}
                  </button>
                )}
              </td>
              <td>
                {editing?.id === p.id && editing.field === 'stock' ? (
                  <span className="admin-edit-cell">
                    <input type="number" min="0" value={editValue} onChange={(e) => setEditValue(e.target.value)} autoFocus />
                    <button onClick={saveEdit}>salvar</button>
                    <button onClick={() => setEditing(null)}>cancelar</button>
                  </span>
                ) : (
                  <button className="btn-link" onClick={() => startEdit(p.id, 'stock', String(p.stock))}>
                    {p.stock}
                  </button>
                )}
              </td>
              <td>
                <button className="btn-link danger" onClick={() => handleDelete(p.id)}>excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}