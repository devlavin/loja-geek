import { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { getProduct } from "../api/products";
import { listCategories } from "../api/categories";
import { addToCart } from "../api/cart";
import { getApiErrorMessage } from "../api/error";
import { useAuth } from "../hooks/useAuth";
import { useCart } from "../hooks/useCart";
import type { Product, Category } from "../types/api";
import { formatPrice } from "../utils/format";
import { ProductThumb } from '../components/ProductThumb';

export function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [categoryName, setCategoryName] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [message, setMessage] = useState<{
    type: "error" | "success";
    text: string;
  } | null>(null);
  const [isAdding, setIsAdding] = useState(false);

  const { user } = useAuth();
  const { refreshCart } = useCart();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!id) return;
    let ignore = false;

    Promise.all([getProduct(Number(id)), listCategories()])
      .then(([productData, categories]) => {
        if (ignore) return;
        setProduct(productData);
        const cat = categories.find(
          (c: Category) => c.id === productData.category_id,
        );
        setCategoryName(cat?.name ?? "");
      })
      .catch(() => {
        if (!ignore) setProduct(null);
      })
      .finally(() => {
        if (!ignore) setIsLoading(false);
      });

    return () => {
      ignore = true;
    };
  }, [id]);

  async function handleAddToCart() {
    if (!product) return;

    if (!user) {
      navigate("/login", { state: { from: location } });
      return;
    }

    setMessage(null);
    setIsAdding(true);

    try {
      await addToCart(product.id, quantity);
      await refreshCart();
      setMessage({ type: "success", text: "Produto adicionado ao carrinho." });
    } catch (err) {
      setMessage({
        type: "error",
        text: getApiErrorMessage(
          err,
          "Não foi possível adicionar ao carrinho.",
        ),
      });
    } finally {
      setIsAdding(false);
    }
  }

  if (isLoading) return <p className="page-status">Carregando...</p>;
  if (!product) return <p className="page-status">Produto não encontrado.</p>;

  const outOfStock = product.stock <= 0;

  return (
    <div className="product-detail-page">
      <ProductThumb src={product.image_url} alt={product.name} className="product-detail-thumb" />

      <div className="product-detail-body">
        {categoryName && <div className="product-cat">{categoryName}</div>}
        <h1>{product.name}</h1>
        <div className="product-detail-price">{formatPrice(product.price)}</div>
        {product.description && <p className="product-detail-description">{product.description}</p>}
        <div className="product-detail-description">{product.description}</div>

        {outOfStock ? (
          <div className="stock-note out">esgotado</div>
        ) : product.stock <= 3 ? (
          <div className="stock-note low">últimas {product.stock} unidades</div>
        ) : (
          <div className="stock-note ok">em estoque</div>
        )}

        {!outOfStock && (
          <div className="qty-row">
            <button
              onClick={() => setQuantity((q) => Math.max(1, q - 1))}
              disabled={quantity <= 1}
            >
              -
            </button>
            <span>{quantity}</span>
            <button
              onClick={() => setQuantity((q) => Math.min(product.stock, q + 1))}
              disabled={quantity >= product.stock}
            >
              +
            </button>
          </div>
        )}

        <button
          className="btn-primary"
          onClick={handleAddToCart}
          disabled={outOfStock || isAdding}
        >
          {outOfStock
            ? "Esgotado"
            : isAdding
              ? "Adicionando..."
              : "Adicionar ao carrinho"}
        </button>

        {message && (
          <p
            className={message.type === "error" ? "auth-error" : "success-note"}
          >
            {message.text}
            {message.type === "success" && (
              <>
                {" "}
                — <a href="/carrinho">ver carrinho</a>
              </>
            )}
          </p>
        )}
      </div>
    </div>
  );
}
