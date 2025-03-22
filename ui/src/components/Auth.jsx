import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import LoginForm from "./LoginForm";
import ResetPasswordForm from "./ResetPasswordForm.jsx";

const Auth = () => {
    const [isReset, setIsReset] = useState(false);
    const { logIn, resetPassword } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (email, password) => {
        await logIn(email, password);
        navigate("/");
    };

    const handleReset = async (email) => {
        await resetPassword(email);
        navigate("/login");
    };

    return isReset ? (
        <ResetPasswordForm onSwitch={() => setIsReset(false)} onReset={handleReset} />
    ) : (
        <LoginForm onSwitch={() => setIsReset(true)} onLogin={handleLogin} />
    );
};

export default Auth;