import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/forgot-password/';

const forgotPasswordService = async (email) => {
    const response = await axios.post(API_URL, { email });

    console.log(response.data);
};

export default forgotPasswordService;
