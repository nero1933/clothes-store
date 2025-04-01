import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import LogoutButton from "./LogoutButton.jsx";


const Header = () => {
    const { id, name, is_guest } = useSelector((state) => state.auth);

    // console.log(id, name, is_guest);

    const displayForUser =
        <>
            <Link to="/account">{name}</Link>
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