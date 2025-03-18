import Header from "../components/Header.jsx";
import DropdownMenu from "../components/DropdownMenu.jsx";
import ProductList from "../components/ProductList.jsx";
import Footer from "../components/Footer.jsx";
import useProducts from "../hooks/useProducts.js";

const Home = () => {
    const { products, loading, error } = useProducts();

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
      <>
          <Header/>
          <DropdownMenu/>
          <div>
              <h1>Products</h1>
              <ProductList products={products}/>
          </div>
          <Footer/>
      </>
  );
};

export default Home;