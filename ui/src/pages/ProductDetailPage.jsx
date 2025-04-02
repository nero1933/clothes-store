import useProductDetail from "../hooks/useProductDetail.js";
import ProductDetail from "../components/ProductDetail.jsx";
import { useParams } from "react-router-dom";

const ProductDetailPage = () => {
    const { slug } = useParams(); // Extract slug from the URL

    // Fetch the product details using the custom hook
    const { product, error, isLoading } = useProductDetail(slug);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
      <>
          <h1>Products</h1>
          <ProductDetail product={product}/>
      </>
  );
};

export default ProductDetailPage;