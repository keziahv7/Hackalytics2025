import React from 'react';
import { Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import NewEntry from './pages/newentry';
import Login from './pages/Login';

function PrivateRoute({ element }) {
  return localStorage.getItem("token") ? element : <Navigate to="/login" />;
}

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={
          <div className="home-container">
            <h1>Welcome to Your Journal</h1>
            <p>Capture your thoughts, reflect on your day, and track your progress.</p>
            <div className="button-container">
              <Link to="/new-entry">
                <button className="nav-button">New Entry</button>
              </Link>
              <Link to="/view-entries">
                <button className="nav-button">View Entries</button>
              </Link>
              <Link to="/profile">
                <button className="nav-button">Profile</button>
              </Link>
              <button onClick={() => { localStorage.removeItem("token"); window.location.reload(); }} className="nav-button">
                Logout
              </button>
            </div>
          </div>
        }/>
        <Route path="/new-entry" element={<PrivateRoute element={<NewEntry />} />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}

export default App;
