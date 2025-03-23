import { React, useState } from "react";
import signInService from "../services/signInService.js";

function SignInForm() {
    const [email, setEmail] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [isRegistered, setIsRegistered] = useState(false);

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setMessage("");

        if (!email || !firstName || !lastName || !password || !confirmPassword) {
            setError("Enter all credentials!");
            return;
        }

        try {
            await signInService(
                email, firstName, lastName, password, confirmPassword);

            setIsRegistered(true);

            // console.log('Sign-in successful');

        } catch (error) {
            if (error.status === 406) {
                setError("Email already exists!");
            } else {
                setError("An unexpected error occurred");
                console.error("Sign-in error:", error);
            }

        }
    }

    return (
        <div>
            {isRegistered ? (
                <div>
                    <p>Successfully registered</p>
                    <p>Welcome, {firstName}!</p>
                    <p>Check your email for confirmation link</p>
                </div>
            ) : (
                <div>
                    <h2>Enter credentials</h2>

                    {error && <p>{error}</p>}
                    {message && <p>{message}</p>}

                    <form onSubmit={handleSubmit}>
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) =>
                                setEmail(e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="First Name"
                            value={firstName}
                            onChange={(e) =>
                                setFirstName(e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Last Name"
                            value={lastName}
                            onChange={(e) =>
                                setLastName(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) =>
                                setPassword(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={(e) =>
                                setConfirmPassword(e.target.value)}
                        />

                        <button type="submit">SignIn</button>
                    </form>
                </div>
            )}
        </div>
    )
}

export default SignInForm;
