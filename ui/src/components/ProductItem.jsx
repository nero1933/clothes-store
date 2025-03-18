const formatPrice = (price) => (price / 100).toFixed(2);

const ProductItem = ({ product }) => {
  // Extract all actual prices (discounted or original)
  const prices = product.product_items.map(item =>
    item.discount_price ? parseFloat(item.discount_price) : item.price
  );

  // Find the min and max price
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);

  return (
    <li>
      <h2>{product.name}</h2>
      <p>Brand: {product.brand}</p>
      <p>Category: {product.category}</p>
      <p>Price: ${minPrice === maxPrice ? formatPrice(minPrice) : `${formatPrice(minPrice)} - ${formatPrice(maxPrice)}`}</p>
    </li>
  );
};

export default ProductItem;