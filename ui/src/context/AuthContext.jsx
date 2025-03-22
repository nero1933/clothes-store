import { createContext, useContext, useState, useEffect } from "react";
import { logInUser } from "../services/logInUserService.js";
import { logoutUser } from "../services/logoutUserService.js";
import resetPasswordService from "../services/resetPasswordService.js";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState(() => {
        const storedAuth = localStorage.getItem("auth");
        return storedAuth ? JSON.parse(storedAuth) : { id: null, name: "Guest", is_guest: true };
    });

    useEffect(() => {
        // console.log("Auth state updated:", auth);

        localStorage.setItem("auth", JSON.stringify(auth));
    }, [auth]);

    const logIn = async (email, password) => {
        try {
            const { access_token, id, name, is_guest } = await logInUser(email, password);

            localStorage.setItem("access_token", access_token);
            setAuth({ id, name, is_guest });
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    const logout = async () => {
        try {
            await logoutUser();
        } catch (error) {
            console.error("Logout failed:", error);
        } finally {
            localStorage.removeItem("access_token");
            localStorage.removeItem("auth");
            setAuth({ id: null, name: "Guest", is_guest: true });
        }
    };

    const resetPassword = async (email) => {
        try {
            await resetPasswordService(email)
        } catch (error) {
            console.error("Password reset failed:", error);
        }

        console.log("Sending reset email to:", email);
    };

    return (
        <AuthContext.Provider value={{ ...auth, logIn, logout, resetPassword }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
