import { Link } from "react-router-dom";

const formatPrice = (price) => (price / 100).toFixed(2);

const ProductCard = ({ product }) => {

    // Extract all actual prices (discounted or original)
    const prices = product.product_items.map(item =>
        item.discount_price ? parseFloat(item.discount_price) : item.price
    );

    const main_images = product.product_items
        .flatMap(item => item.images) // Extract images array from each product item
        .filter(image => image.is_main) // Keep only main images
        .map(image => ({
            name: image.name,
            url: image.url
        }));

    // Find the min and max price
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);

    return (
        <li>
            <Link to={`/products/${product.slug}`}>
                <h2>{product.name}</h2>
                <div>
                    {main_images.map((image) => (
                        <img
                            key={image.url}
                            src={image.url}
                            alt={image.url}
                            loading="lazy"
                        />
                    ))}
                </div>
                <p>Brand: {product.brand}</p>
                <p>Category: {product.category}</p>
                <p>
                    Price: ${minPrice === maxPrice
                        ? formatPrice(minPrice)
                        : `${formatPrice(minPrice)} - ${formatPrice(maxPrice)}`}
                </p>
            </Link>
        </li>
    );
};

export default ProductCard;