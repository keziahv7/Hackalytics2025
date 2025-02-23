import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ isLoggedIn }) {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                {isLoggedIn && <li><Link to="/journal">Journal</Link></li>}
                <li><Link to="/games">Games</Link></li>
                {isLoggedIn ? (
                    <li><Link to="/logout">Logout</Link></li>
                ) : (
                    <li><Link to="/login">Login</Link></li>
                )}
            </ul>
        </nav>
    );
}

export default Navbar;
