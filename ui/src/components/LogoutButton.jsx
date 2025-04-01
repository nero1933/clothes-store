import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { logout } from "../features/authSlice";


const LogoutButton = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch()

    const handleLogout = async () => {
        try {
            await dispatch(logout()).unwrap();
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
