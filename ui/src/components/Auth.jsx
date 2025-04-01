import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { forgotPassword, logIn } from "../features/authSlice.jsx";
import LoginForm from "./LoginForm.jsx";
import ForgotPasswordForm from "./ForgotPasswordForm.jsx";

const Auth = () => {
    const [isForgot, setIsForgot] = useState(false);

    const dispatch = useDispatch();
    const navigate = useNavigate();

    // Get any error or loading state from Redux store
    const { error, loading } = useSelector((state) => state.auth);

    const handleLogin = async (email, password) => {
        try {
            await dispatch(logIn({ email, password })).unwrap();
            navigate("/");
        } catch (error) {
            console.log("Login failed:", error);
        }
    };

    const handleForgot = async (email) => {
        try {
            // Returns a message which will be displayed after form will be submitted.
            return await dispatch(forgotPassword(email)).unwrap();
        } catch (error) {
            console.log("Password reset failed:", error);
        }
    };

    return isForgot ? (
        <ForgotPasswordForm onSwitch={() => setIsForgot(false)} onForgot={handleForgot} />
    ) : (
        <LoginForm onSwitch={() => setIsForgot(true)} onLogin={handleLogin} />
    );
};

export default Auth;
