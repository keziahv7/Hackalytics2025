import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import NewEntry from './pages/newentry';

function App() {
  return (
    <div className="app">
      <Routes>
        {/* Home Page */}
        <Route
          path="/"
          element={
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
              </div>
            </div>
          }
        />
        
        {/* New Entry Page */}
        <Route path="/new-entry" element={<NewEntry />} />
      </Routes>
    </div>
  );
}

export default App;
