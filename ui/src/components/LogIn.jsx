import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { jwtDecode } from "jwt-decode";


const LogIn = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const { setAuth } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email || !password) {
            setError("Enter all credentials!");
            return;
        }

        try {
            const response = await axios.post("http://localhost:8000/api/v1/login/", {
                email,
                password
            });

            const access_token = response.data.access_token;
            localStorage.setItem("access_token", access_token);
            console.log("Successful authorization!", access_token);

            const decoded = jwtDecode(access_token);
            setAuth({ user_id: decoded.user_id, is_guest: false });

            navigate("/");

        } catch (error) {
            setError("Wrong email or password");
            console.error("LogIn error:", error);
        }
    };

    return (
        <div>
            <h2>Authorization</h2>

            {error && <p>{error}</p>}

            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">
                    Login
                </button>
            </form>

        </div>
    );
};

export default LogIn;