import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './Navbar';  // Ensure Navbar.js is inside src/
import Home from './Home';  // Ensure Home.js is inside src/
import Login from './Login';  // Ensure Login.js is inside src/
import Signup from './Signup';  // Ensure Signup.js is inside src/
import Dashboard from './Dashboard';  // Ensure Dashboard.js is inside src/

import './App.css';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleLogin = (username, password) => {
        if (username === 'Amna' && password === 'Amna') {
            setIsLoggedIn(true);
        } else {
            alert('Wrong username or password. Please try again.');
        }
    };

    return (
        <Router>
            <div className="App">
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login onLogin={handleLogin} />} />
                    <Route path="/signup" element={<Signup />} />
                    <Route path="/dashboard" element={isLoggedIn ? <Dashboard /> : <Login />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
