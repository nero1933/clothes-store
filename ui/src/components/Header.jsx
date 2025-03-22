import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import LogoutButton from "./LogoutButton.jsx";
import React from "react";

const Header = () => {
    const { id, name, is_guest } = useAuth();
    console.log("Header render:", id, name, is_guest);

    return (
        <header>
            <nav>
                {is_guest ? (
                    <>
                        <Link to="/signin">Sign in</Link>
                        <Link to="/login">Login</Link>
                    </>
                ) : (
                    <>
                        <p>{`Hello user: ${name}, id: ${id}`}</p>
                        <LogoutButton />
                    </>
                )}
            </nav>
        </header>
    );
};

export default Header;