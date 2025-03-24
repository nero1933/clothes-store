import axios from "axios";

const API_URL = "http://localhost:8000/api/v1/register/confirmation/";

const activateAccountService = async (token) => {
    const response = await axios.post(`${API_URL}${token}/`, )
}

export default activateAccountService;