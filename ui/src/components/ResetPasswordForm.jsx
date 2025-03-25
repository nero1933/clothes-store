import { React, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import resetPasswordService from "../services/ResetPasswordService.js";

const ResetPasswordForm = () => {
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const { token } = useParams();

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");
        setError("");

        if (!password || !confirmPassword) {
            setError("Enter all credentials!");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }

        if (password.length < 8) {
            setError("Password must be at least 8 characters!");
            return
        }

        setLoading(true);
        try {
            await resetPasswordService(token, password, confirmPassword);
            setMessage("Password was reset successfully.");
            setTimeout(() => navigate("/"), 3000);
        } catch (err) {
            const errorMsg = err.response?.data?.detail || "Something went wrong. Try again.";
            setError(errorMsg);
        }
    };

    return (
        <div>
            {message && <p>{message}</p>}
            {error && <p>{error}</p>}

            <form onSubmit={handleSubmit}>
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) =>
                        setPassword(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Confirm password"
                    value={confirmPassword}
                    onChange={(e) =>
                        setConfirmPassword(e.target.value)}
                />

                <button type="submit" disabled={loading}>
                    {loading ? "Processing..." : "Set Password"}
                </button>
            </form>
        </div>
    )
};

export default ResetPasswordForm;