import { useEffect, useState } from "react";
import { listProducts } from "../api/products";
import { listCategories } from "../api/categories";
import type { Product, Category } from "../types/api";
import { ProductCard } from "../components/ProductCard";

export function ProductList() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [search, setSearch] = useState("");
  const [categoryName, setCategoryName] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    listCategories()
      .then(setCategories)
      .catch(() => {});
  }, []);

  useEffect(() => {
    let ignore = false;

    const timeout = setTimeout(() => {
      setIsLoading(true);

      listProducts({
        name: search || undefined,
        category: categoryName || undefined,
      })
        .then((data) => {
          if (!ignore) {
            setProducts(data);
            setIsLoading(false);
          }
        })
        .catch(() => {
          if (!ignore) setIsLoading(false);
        });
    }, 300);

    return () => {
      ignore = true;
      clearTimeout(timeout);
    };
  }, [search, categoryName]);

  return (
    <div className="product-list-page">
      <div className="filters">
        <input
          type="text"
          placeholder="Buscar produto..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          value={categoryName}
          onChange={(e) => setCategoryName(e.target.value)}
        >
          <option value="">Todas as categorias</option>
          {categories.map((c) => (
            <option key={c.id} value={c.name}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {isLoading ? (
        <p>Carregando...</p>
      ) : products.length === 0 ? (
        <p>Nenhum produto encontrado.</p>
      ) : (
        <div className="product-grid">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      )}
    </div>
  );
}
