import { useState, useEffect } from 'react';
import axios from 'axios';

const useProducts = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
    axios.get('http://localhost:8000/api/v1/products/')
        .then((response) => {
            setProducts(response.data);
        })
        .catch((error) => {
            console.error('Error while fetching data', error);
            setError(error);
        })
        .finally(() => {
            setLoading(false);
        });
    }, []);

    return { products, loading, error };
};

export default useProducts;
