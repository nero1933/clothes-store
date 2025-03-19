import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState({ user_id: null, is_guest: true });

    useEffect(() => {
        const token = localStorage.getItem("access_token");

        if (token) {
            try {
                const decoded = jwtDecode(token);
                setAuth({ user_id: decoded.user_id, is_guest: false });
            } catch (error) {
                console.error(error);
            }
        }
    }, []);

    return (
        <AuthContext.Provider value={{ ...auth, setAuth }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);