import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/login/';

export const logInUser = async (email, password) => {
    const response = await axios.post(API_URL, { email, password });

    console.log(response.data);

    const { access_token, id, name, is_guest } = response.data;

    console.log(access_token, id, name, is_guest);

    return { access_token, id, name, is_guest };
}