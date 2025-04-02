import useProductDetail from "../hooks/useProductDetail.js";
import { useParams } from "react-router-dom"; // React Router hook to get URL params


const formatPrice = (price) => (price / 100).toFixed(2);

const ProductDetailPage = () => {
    const { slug } = useParams(); // Extract slug from the URL

    // Fetch the product details using the custom hook
    const { data, error, isLoading } = useProductDetail(slug);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div>
            <h2>{data.name}</h2>
            <p>{data.description}</p>
            {/* Render other product details here */}
        </div>
    );
};

export default ProductDetailPage;