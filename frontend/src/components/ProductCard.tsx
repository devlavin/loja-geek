import { Link } from 'react-router-dom';
import type { Product } from '../types/api';
import { formatPrice } from '../utils/format';
import { ProductThumb } from './ProductThumb';

export function ProductCard({ product }: { product: Product }) {
  const outOfStock = product.stock <= 0;

  return (
    <Link to={`/produtos/${product.id}`} className="product-card">
      <ProductThumb src={product.image_url} alt={product.name} className="product-thumb" />
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