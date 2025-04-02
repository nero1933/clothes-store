import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/products/';

export const fetchProducts = async () => {
    const { data } = await axios.get(API_URL);
    return data;
};

export default { fetchProducts };
