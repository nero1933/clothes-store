import { Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage.jsx";
import SignInPage from "../pages/SignInPage.jsx";
import LogInPage from "../pages/LogInPage.jsx";
import ActivateAccountPage from "../pages/ActivateAccountPage.jsx";
import ResetPasswordPage from "../pages/ResetPasswordPage.jsx";
import NotFoundPage from "../pages/NotFoundPage.jsx";
import AccountPage from "../pages/AccountPage.jsx";
import PrivateRoute from "./PrivateRoutes.jsx";
import Layout from "../pages/layout/Layout.jsx";
import ProductDetailPage from "../pages/ProductDetailPage.jsx";

const AppRoutes = () => {
    return (
        <Routes>
            {/* Public routes */}
            <Route path="/" element={<Layout />}>
                <Route index element={<HomePage />} />
                <Route path = "products/:slug" element={<ProductDetailPage />} />
            </Route>

            <Route path="/signin" element={<SignInPage />} />
            <Route path="/login" element={<LogInPage />} />
            <Route path="/activate/:token" element={<ActivateAccountPage />} />
            <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
            <Route path="*" element={<NotFoundPage />} />

            {/* Private routes */}
            <Route path="/account" element={<PrivateRoute element={<AccountPage />} />} />
        </Routes>
    );
};

export default AppRoutes;