import React, { useState } from 'react';

function Journal() {
    const [entry, setEntry] = useState('');
    const [previousEntries, setPreviousEntries] = useState([]);

    const saveEntry = () => {
        setPreviousEntries([...previousEntries, entry]);
        setEntry('');
    };

    return (
        <div>
            <h2>Daily Journal</h2>
            <textarea onChange={(e) => setEntry(e.target.value)} value={entry} />
            <button onClick={saveEntry}>Save</button>
            <ul>
                {previousEntries.map((note, index) => <li key={index}>{note}</li>)}
            </ul>
        </div>
    );
}

export default Journal;
