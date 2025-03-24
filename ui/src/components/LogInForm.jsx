import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LogInForm = ({ onSwitch, onLogin }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email || !password) {
            setError("Enter all credentials!");
            return;
        }

        try {
            await onLogin(email, password);
            navigate("/");
        } catch (err) {
            setError(err.message);
            console.error("Log in (Form) error:", err);
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

            <button onClick={onSwitch}>Forgot Password?</button>

        </div>
    );
};

export default LogInForm;