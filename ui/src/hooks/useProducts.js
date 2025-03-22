import { useState, useEffect } from 'react';
import { fetchProducts } from '../services/productsService';

const useProducts = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadProducts = async () => {
            try {
                const data = await fetchProducts();
                setProducts(data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        loadProducts().catch(console.error);
    }, []);

    return { products, loading, error };
};

export default useProducts;