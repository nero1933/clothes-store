import { useState } from "react";

const ResetPasswordForm = ({ onSwitch, onReset }) => {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setMessage("");

        if (!email) {
            setError("Enter your email!");
            return;
        }

        const responseMessage = await onReset(email);
        setMessage(responseMessage);
    };

    return (
        <div>
            <h2>Reset Password</h2>
            {error && <p>{error}</p>}
            {message && <p>{message}</p>}

            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <button type="submit">Send Reset Link</button>
            </form>

            <button onClick={onSwitch}>Back to Login</button>
        </div>
    );
};

export default ResetPasswordForm;
