import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import {
  listProducts,
  createProduct,
  updateProduct,
  updateProductStock,
  deleteProduct,
} from "../../api/products";
import { listCategories } from "../../api/categories";
import { getApiErrorMessage } from "../../api/error";
import type { Product, Category } from "../../types/api";
import { formatPrice } from "../../utils/format";
import { ProductThumb } from "../../components/ProductThumb";

interface FormState {
  name: string;
  description: string;
  price: string;
  stock: string;
  category_id: string;
  image_url: string;
}

const EMPTY_FORM: FormState = {
  name: "",
  description: "",
  price: "",
  stock: "",
  category_id: "",
  image_url: "",
};

export function AdminProducts() {
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");

  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const [formMode, setFormMode] = useState<"closed" | "create" | number>(
    "closed",
  );
  const [form, setForm] = useState<FormState>(EMPTY_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [stockEditId, setStockEditId] = useState<number | null>(null);
  const [stockValue, setStockValue] = useState("");

  function categoryName(id: number) {
    return categories.find((c) => c.id === id)?.name ?? "—";
  }

  function load() {
    Promise.all([
      listProducts({
        name: search || undefined,
        category: categoryFilter || undefined,
      }),
      listCategories(),
    ])
      .then(([p, c]) => {
        setProducts(p);
        setCategories(c);
      })
      .catch((err) =>
        setError(
          getApiErrorMessage(err, "Não foi possível carregar os produtos."),
        ),
      )
      .finally(() => setIsLoading(false));
  }

  useEffect(() => {
    const timeout = setTimeout(load, 300);
    return () => clearTimeout(timeout);
  }, [search, categoryFilter]);

  function openCreate() {
    setForm(EMPTY_FORM);
    setFormMode("create");
  }

  function openEdit(p: Product) {
    setForm({
      name: p.name,
      description: p.description ?? "",
      price: p.price,
      stock: String(p.stock),
      category_id: String(p.category_id),
      image_url: p.image_url ?? "",
    });
    setFormMode(p.id);
  }

  function closeForm() {
    setFormMode("closed");
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    const payload = {
      name: form.name,
      description: form.description || undefined,
      price: Number(form.price),
      stock: Number(form.stock),
      category_id: Number(form.category_id),
      image_url: form.image_url || undefined,
    };

    try {
      if (formMode === "create") {
        await createProduct(payload);
      } else if (typeof formMode === "number") {
        await updateProduct(formMode, payload);
      }
      closeForm();
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, "Não foi possível salvar o produto."));
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleStockSave(id: number) {
    setError("");
    try {
      await updateProductStock(id, Number(stockValue));
      setStockEditId(null);
      load();
    } catch (err) {
      setError(
        getApiErrorMessage(err, "Não foi possível atualizar o estoque."),
      );
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Excluir este produto?")) return;
    setError("");
    try {
      await deleteProduct(id);
      load();
    } catch (err) {
      setError(getApiErrorMessage(err, "Não foi possível excluir o produto."));
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <h1>Produtos</h1>
        {formMode === "closed" && (
          <button className="btn-primary" onClick={openCreate}>
            Novo produto
          </button>
        )}
      </div>

      {error && <p className="auth-error">{error}</p>}

      <div className="filters">
        <input
          type="text"
          placeholder="Buscar produto..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          <option value="">Todas as categorias</option>
          {categories.map((c) => (
            <option key={c.id} value={c.name}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {formMode !== "closed" && (
        <form onSubmit={handleSubmit} className="admin-form-panel">
          <h2>{formMode === "create" ? "Novo produto" : "Editar produto"}</h2>

          <div className="form-group">
            <label>Nome</label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label>Descrição</label>
            <textarea
              value={form.description}
              onChange={(e) =>
                setForm({ ...form, description: e.target.value })
              }
              rows={3}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Preço</label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                value={form.price}
                onChange={(e) => setForm({ ...form, price: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Estoque</label>
              <input
                type="number"
                min="0"
                value={form.stock}
                onChange={(e) => setForm({ ...form, stock: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Categoria</label>
            <select
              value={form.category_id}
              onChange={(e) =>
                setForm({ ...form, category_id: e.target.value })
              }
              required
            >
              <option value="">Selecione</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>URL da imagem</label>
            <input
              type="text"
              value={form.image_url}
              onChange={(e) => setForm({ ...form, image_url: e.target.value })}
              placeholder="https://..."
            />
          </div>

          {form.image_url && (
            <ProductThumb
              src={form.image_url}
              alt="Pré-visualização"
              className="admin-form-preview"
            />
          )}

          <div className="form-actions">
            <button
              className="btn-primary"
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Salvando..." : "Salvar"}
            </button>
            <button type="button" className="btn-link" onClick={closeForm}>
              Cancelar
            </button>
          </div>
        </form>
      )}

      <table className="admin-table">
        <thead>
          <tr>
            <th></th>
            <th>Nome</th>
            <th>Categoria</th>
            <th>Preço</th>
            <th>Estoque</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>
                <ProductThumb
                  src={p.image_url}
                  alt={p.name}
                  className="admin-thumb"
                />
              </td>
              <td>{p.name}</td>
              <td>{categoryName(p.category_id)}</td>
              <td>{formatPrice(p.price)}</td>
              <td>
                {stockEditId === p.id ? (
                  <span className="admin-edit-cell">
                    <input
                      type="number"
                      min="0"
                      value={stockValue}
                      onChange={(e) => setStockValue(e.target.value)}
                      autoFocus
                    />
                    <button onClick={() => handleStockSave(p.id)}>
                      salvar
                    </button>
                    <button onClick={() => setStockEditId(null)}>
                      cancelar
                    </button>
                  </span>
                ) : (
                  <button
                    className="btn-link"
                    onClick={() => {
                      setStockEditId(p.id);
                      setStockValue(String(p.stock));
                    }}
                  >
                    {p.stock}
                  </button>
                )}
              </td>
              <td>
                <button className="btn-link" onClick={() => openEdit(p)}>
                  editar
                </button>
                <button
                  className="btn-link danger"
                  onClick={() => handleDelete(p.id)}
                >
                  excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
