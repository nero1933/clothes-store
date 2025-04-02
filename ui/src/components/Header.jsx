import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import LogoutButton from "./LogoutButton.jsx";
import DropdownMenu from "./DropdownMenu.jsx";


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
                <Link to="/">Main Page   </Link>
                {is_guest ? displayForGuest : displayForUser}
            </nav>
            <nav>
                <DropdownMenu/>
            </nav>
        </header>
    )
}

export default Header;