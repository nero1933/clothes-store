import { Link } from "react-router-dom";


const Header = () => {
    return(
        <header>
            <nav>
                <Link to="/signin">Sign in</Link>
                <Link to="/login">Login</Link>
            </nav>
        </header>
    )
}

export default Header;