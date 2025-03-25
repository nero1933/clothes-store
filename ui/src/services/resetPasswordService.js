import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1/password-reset/new-password/'

const resetPasswordService = async (token, password, password_confirmation) => {
    try {
        const response = await axios.patch(`${API_URL}${token}/`, {
            password: password,  
            password_confirmation: password_confirmation,  // Ensure this field is sent!
        });

        console.log("Response:", response.data);
        return response.data;
    } catch (err) {
        console.error("Error:", err.response?.data || err.message);

        throw new Error(
            err.response?.data?.non_field_errors?.[0] || "Something went wrong. Try again."
        );
    }
};

export default resetPasswordService;
