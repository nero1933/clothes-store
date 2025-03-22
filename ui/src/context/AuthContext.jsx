import { createContext, useContext, useState, useEffect } from "react";
import { logInUser } from "../services/logInUserService.js";
import { logoutUser } from "../services/logoutUserService.js";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState(() => {
        const storedAuth = localStorage.getItem("auth");
        return storedAuth ? JSON.parse(storedAuth) : { id: null, name: "Guest", is_guest: true };
    });

    useEffect(() => {
        console.log("Auth state updated:", auth);
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

    return (
        <AuthContext.Provider value={{ ...auth, logIn, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
