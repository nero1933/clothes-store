import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/register/user/';

const signInService = async (email, first_name, last_name, password, password_confirmation) => {
    const response = await axios.post(API_URL,
        { email, first_name, last_name, password, password_confirmation });

    // console.log(response.data);
};

export default signInService;
