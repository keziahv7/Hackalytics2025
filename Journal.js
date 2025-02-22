import React, { useState } from "react";
import axios from "axios";

const Journal = ({ token }) => {
  const [text, setText] = useState("");
  const [entries, setEntries] = useState([]);

  const handleSaveEntry = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/store_entry", {
        token,
        text,
      });
      alert(response.data.message);
    } catch (error) {
      alert("Error: " + error.response.data.error);
    }
  };

  const fetchEntries = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/get_entries", { token });
      setEntries(response.data.entries);
    } catch (error) {
      alert("Error fetching entries: " + error.response.data.error);
    }
  };

  return (
    <div>
      <h2>Journal</h2>
      <textarea onChange={(e) => setText(e.target.value)} placeholder="Write your journal entry here..." />
      <button onClick={handleSaveEntry}>Save Entry</button>
      <button onClick={fetchEntries}>Show My Entries</button>
      
      <h3>Previous Entries</h3>
      {entries.map((entry, index) => (
        <div key={index}>
          <p>{entry.text}</p>
          <p>Stress Level: {entry.stress_level}</p>
          <p>Suggestion: {entry.suggestion}</p>
          <p>{entry.timestamp}</p>
        </div>
      ))}
    </div>
  );
};

export default Journal;
