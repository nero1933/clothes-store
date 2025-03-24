import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import activateAccountService from "../services/activateAccountService.js";

const ActivateAccount = () => {
    const { token } = useParams();
    const navigate = useNavigate();
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
       const activateUser = async () => {
           try {
               await activateAccountService(token)
               setMessage("Account activated successfully")
               setTimeout(() => navigate("/login"), 3000);
           } catch (err) {
               setError("Activation failed. The link may be invalid or expired.");
               console.error("Activation error:", err.response?.data || err.message);
           }
        };

       if (token) activateUser();
    }, [token, navigate]);

    return (
        <div>
            <h2>Account Activation</h2>
            {message && <p>{message}</p>}
            {error && <p>{error}</p>}
        </div>
    );
}

export default ActivateAccount;