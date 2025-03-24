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
        } catch (err) {
                console.error("Log in (Context) error:", err);
            if (err.response && err.response.status === 401) {
                throw new Error("Invalid email or password.");
            } else if (err.response && err.response.status === 403) {
                throw new Error("Your account is not activated. Please check your email.");
            }
        }
    };

    const logout = async () => {
        try {
            await logoutUser();
        } catch (err) {
            console.error("Logout (Context) Error):", err);
        } finally {
            localStorage.removeItem("access_token");
            localStorage.removeItem("auth");
            setAuth({ id: null, name: "Guest", is_guest: true });
        }
    };

    const resetPassword = async (email) => {
        try {
            await resetPasswordService(email)
            return "If this email is registered, you will receive a password reset link."
        } catch (err) {
            // Do not show user that the email does not exist in db for security reasons.
            if (err.response?.status === 404) {
                console.log("Reset Password (Form) Error:", 404);
                return "If this email is registered, you will receive a password reset link.";
            } else {
                console.error("Reset Password (Form) Error:", err);
                return "Something went wrong. Please try again later.";
            }
        }
    };

    return (
        <AuthContext.Provider value={{ ...auth, logIn, logout, resetPassword }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
