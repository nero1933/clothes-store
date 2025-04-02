import ProductList from "../components/ProductList.jsx";
import useProducts from "../hooks/useProducts.js";

const HomePage = () => {
    const { products, loading, error } = useProducts();

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
      <>
          <h1>Products</h1>
          <ProductList products={products}/>
      </>
  );
};

export default HomePage;