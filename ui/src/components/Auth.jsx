import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LoginForm from "./LoginForm.jsx";
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
        // Returns a message which will bw displayed after form will be submitted.
        return await resetPassword(email);
    };

    return isReset ? (
        <ResetPasswordForm onSwitch={() => setIsReset(false)} onReset={handleReset} />
    ) : (
        <LoginForm onSwitch={() => setIsReset(true)} onLogin={handleLogin} />
    );
};

export default Auth;
