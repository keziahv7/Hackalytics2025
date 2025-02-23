import React, { useState } from 'react';

function Features() {
    const [journalText, setJournalText] = useState('');
    const [mood, setMood] = useState('');

    const handleJournalChange = (e) => {
        setJournalText(e.target.value);
    };

    const suggestPlaylist = () => {
        if (mood.toLowerCase().includes('depressed')) {
            return ["Happy Song 1", "Upbeat Song 2"]; // Replace with actual song suggestions
        } else if (mood.toLowerCase().includes('exhausted')) {
            return ["Relaxing Song 1", "Soothing Song 2"]; // Replace with actual song suggestions
        } else {
            return ["General Mood Song 1", "General Mood Song 2"];
        }
    };

    return (
        <div className="features-container">
            <h2>Features</h2>

            <div className="feature">
                <h3>Wearable Connect</h3>
                <p>Integrate with your favorite wearable to get real-time health insights.</p>
            </div>

            <div className="feature">
                <h3>Your Weekly Data</h3>
                <p>Get a summary of how you’ve been feeling and performing throughout the week.</p>
            </div>

            <div className="feature">
                <h3>Mood-Based Playlists</h3>
                <input type="text" placeholder="Enter your mood" value={mood} onChange={(e) => setMood(e.target.value)} />
                <ul>
                    {suggestPlaylist().map((song, index) => (
                        <li key={index}>{song}</li>
                    ))}
                </ul>
            </div>

            <div className="feature">
                <h3>Write a Journal</h3>
                <textarea value={journalText} onChange={handleJournalChange} placeholder="Write your journal entry here..."></textarea>
            </div>

            <div className="feature">
                <h3>More Features</h3>
                <p>Discover other tools and techniques to improve your mental health.</p>
            </div>
        </div>
    );
}

export default Features;