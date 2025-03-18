import { useState } from "react";
import axios from "axios";


const Authorization = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

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

            const accessToken = response.data.access_token;
            localStorage.setItem("access_token", accessToken);

            console.log("Successful authorization!", accessToken);
            setError("");
        } catch (error) {
            console.error("Authorization error:", error);
            setError("Wrong email or password");
        }
    };

    return (
        <div>
            <h2>Авторизация</h2>

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
                    Войти
                </button>
            </form>

        </div>
    );
};

export default Authorization;