import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import SignIn from "../pages/SignIn";
import Login from "../pages/Login";
import {AuthProvider} from "../context/AuthContext.jsx";

const AppRoutes = () => {
    return (
        <AuthProvider>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/signin" element={<SignIn />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </AuthProvider>
    );
};

export default AppRoutes;