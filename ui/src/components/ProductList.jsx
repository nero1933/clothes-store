import ProductCard from "./ProductCard.jsx";

const ProductList = ({ products }) => {
    return (
        <div>
            <h2>Product List</h2>
            <ul>
                {products.map((product) => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </ul>
        </div>
    );
};

export default ProductList;
