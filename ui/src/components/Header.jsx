import { Link } from "react-router-dom";
import {useAuth} from "../context/AuthContext.jsx";
import LogoutButton from "./LogoutButton.jsx";
import React, { useEffect } from "react";


const Header = () => {
    const { user_id, is_guest } = useAuth();
    console.log(user_id, is_guest);

    const displayForUser =
        <>
            <p>{`Hello user: ${user_id}`}</p>
            <LogoutButton/>
        </>
    const displayForGuest =
        <>
            <Link to="/signin">Sign in</Link>
            <Link to="/login">Login</Link>
        </>


    return(
        <header>
            <nav>
                {is_guest ? displayForGuest : displayForUser}
            </nav>
        </header>
    )
}

export default Header;