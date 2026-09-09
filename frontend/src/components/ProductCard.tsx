import { Link } from "react-router-dom";
import type { Product } from "../types/api";
import { formatPrice } from "../utils/format";

export function ProductCard({ product }: { product: Product }) {
  const outOfStock = product.stock <= 0;

  return (
    <Link to={`/produtos/${product.id}`} className="product-card">
      <div className="product-thumb">
        {product.image_url && (
          <img src={product.image_url} alt={product.name} />
        )}
      </div>
      <div className="product-body">
        <div className="product-name">{product.name}</div>
        <div className="product-price">{formatPrice(product.price)}</div>
        {outOfStock ? (
          <div className="stock-note out">esgotado</div>
        ) : product.stock <= 3 ? (
          <div className="stock-note low">últimas unidades</div>
        ) : (
          <div className="stock-note ok">em estoque</div>
        )}
      </div>
    </Link>
  );
}
