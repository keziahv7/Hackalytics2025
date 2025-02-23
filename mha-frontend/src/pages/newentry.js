import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './newentry.css';

function NewEntry() {
  const [entry, setEntry] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('New Journal Entry:', entry);
    setEntry('');
    navigate('/'); // ✅ Redirects to home after submitting
  };

  return (
    <div className="new-entry-container">
      <h2>New Journal Entry</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="Write your thoughts here..."
          value={entry}
          onChange={(e) => setEntry(e.target.value)}
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
