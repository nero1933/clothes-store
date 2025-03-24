import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LoginForm from "./LoginForm.jsx";
import ForgotPasswordForm from "./ForgotPasswordForm.jsx";

const Auth = () => {
    const [isReset, setIsReset] = useState(false);
    const { logIn, forgotPassword } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (email, password) => {
        await logIn(email, password);
        navigate("/");
    };

    const handleReset = async (email) => {
        // Returns a message which will bw displayed after form will be submitted.
        return await forgotPassword(email);
    };

    return isReset ? (
        <ForgotPasswordForm onSwitch={() => setIsReset(false)} onReset={handleReset} />
    ) : (
        <LoginForm onSwitch={() => setIsReset(true)} onLogin={handleLogin} />
    );
};

export default Auth;
