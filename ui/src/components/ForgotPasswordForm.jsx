import { useState } from "react";

const ForgotPasswordForm = ({ onSwitch, onReset }) => {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setMessage("");

        if (!email) {
            setError("Enter your email!");
            return;
        }

        setLoading(true);

        const responseMessage = await onReset(email);
        setMessage(responseMessage);
    };

    return (
        <div>
            <h2>Forgot Password</h2>
            {error && <p>{error}</p>}
            {message && <p>{message}</p>}

            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Processing..." : "Send Reset Link"}
                </button>
            </form>

            <button onClick={onSwitch}>Back to Login</button>
        </div>
    );
};

export default ForgotPasswordForm;
