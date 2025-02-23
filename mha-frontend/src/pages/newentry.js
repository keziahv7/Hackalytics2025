import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { storeEntry } from '../api'; // Import API functions
import './newentry.css';

function NewEntry() {
  const [text, setText] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const token = localStorage.getItem("token"); // Retrieve token from login
    if (!token) {
      alert("Please log in first.");
      return;
    }

    try {
      const response = await storeEntry(token, text);
      if (response.error) {
        alert(`Error: ${response.error}`);
      } else {
        alert("Entry saved successfully!");
        setText('');
        navigate('/'); // Redirect to home
      }
    } catch (error) {
      console.error("Failed to save entry:", error);
    }
  };

  return (
    <div className="new-entry-container">
      <h2>New Journal Entry</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="Write your thoughts here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        ></textarea>
        <button type="submit" className="submit-button">Save Entry</button>
      </form>
      <button className="back-button" onClick={() => navigate('/')}>
        Back
      </button>
    </div>
  );
}

export default NewEntry;
