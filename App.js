import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const App = () => {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    navigate("/login");
  };

  return (
    <div>
      <h1>Welcome to Your Mental Health Journal</h1>
      {token ? (
        <div>
          <p>You are logged in!</p>
          <button onClick={() => navigate("/journal")}>Go to Journal</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <button onClick={() => navigate("/login")}>Login</button>
      )}
    </div>
  );
};

export default App;
