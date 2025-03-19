import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/api.js";

const LogoutButton = () => {
    const navigate = useNavigate();
    const { setAuth } = useAuth();

    const handleLogout = async () => {
        try {
            await api.post('/logout/');

            localStorage.removeItem("access_token");

            setAuth({ user_id: null, is_guest: true });

            navigate("/");
        } catch (err) {
            console.log(err);
        }
    };

    return (
        <button onClick={handleLogout}>
            logout
        </button>
    )
};

export default LogoutButton;
