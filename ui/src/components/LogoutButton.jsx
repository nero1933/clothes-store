import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/api.js";

const LogoutButton = () => {
    const navigate = useNavigate();
    const { logout } = useAuth()

    const handleLogout = async () => {
        try {
            await logout()
            navigate("/");
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <button onClick={handleLogout}>
            logout
        </button>
    )
};

export default LogoutButton;
