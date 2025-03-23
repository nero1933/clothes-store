import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import SignIn from "../pages/SignIn";
import LogInPage from "../pages/LogIn.jsx";

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signin/activate/:token" element={<ActivateAccount />} />
            <Route path="/login" element={<LogInPage />} />
        </Routes>
    );
};

export default AppRoutes;