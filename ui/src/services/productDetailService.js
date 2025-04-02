import axios from 'axios';

const API_URL = `http://localhost:8000/api/v1/products/`;

export const fetchProductDetail = async (slug) => {
    const { data } = await axios.get(`${API_URL}${slug}/`);
    return data;
};

export default { fetchProductDetail };
