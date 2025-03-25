import { Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage.jsx";
import SignInPage from "../pages/SignInPage.jsx";
import LogInPage from "../pages/LogInPage.jsx";
import ActivateAccountPage from "../pages/ActivateAccountPage.jsx";
import ResetPasswordPage from "../pages/ResetPasswordPage.jsx";

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/signin" element={<SignInPage />} />
            <Route path="/login" element={<LogInPage />} />
            <Route path="/activate/:token" element={<ActivateAccountPage />} />
            <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
        </Routes>
    );
};

export default AppRoutes;