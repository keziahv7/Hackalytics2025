import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css'; // Ensure this file exists and is not empty

function Dashboard() {
    const navigate = useNavigate();

    return (
        <div className="dashboard">
            <h1>Welcome to MindGuard</h1>
            <button onClick={() => navigate('/gamification')}>Gamification</button>
            <button onClick={() => navigate('/playlist')}>Playlist</button>
            <button onClick={() => navigate('/datatrack')}>Data Track</button>
            <button onClick={() => navigate('/journal')}>Daily Journal</button>
            <button onClick={() => navigate('/about')}>About Us</button>
        </div>
    );
}

export default Dashboard;

