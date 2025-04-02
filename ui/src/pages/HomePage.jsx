import ProductList from "../components/ProductList.jsx";
import useProducts from "../hooks/useProducts.js";

const HomePage = () => {
    const { data: products, isLoading, isError, error } = useProducts();

    if (isLoading) return <p>Loading...</p>;
    if (isError) return <p>Error: {error.message}</p>;

    return (
      <>
          <h1>Products</h1>
          <ProductList products={products}/>
      </>
  );
};

export default HomePage;
