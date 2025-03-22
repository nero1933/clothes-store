import API from "../api/api.js";

const API_ENDPOINT = 'api/v1/logout/';

export const logoutUser = async () => {
    const response = await API.post(API_ENDPOINT);

    console.log(response.data);
}
