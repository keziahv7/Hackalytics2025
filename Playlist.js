import React, { useState } from 'react';

function Playlist() {
    const [mood, setMood] = useState('');
    const [songs, setSongs] = useState([]);

    const moodSongs = {
        happy: ['Shake It Off', 'Uptown Funk', 'Despacito'],
        exhausted: ['Best Day of My Life', 'I Wanna Dance with Somebody', 'Girls Just Wanna Have Fun']
    };

    const generatePlaylist = () => {
        setSongs(moodSongs[mood.toLowerCase()] || ['No songs found']);
    };

    return (
        <div>
            <h2>Music Playlist</h2>
            <input type="text" placeholder="Enter your mood" onChange={(e) => setMood(e.target.value)} />
            <button onClick={generatePlaylist}>Get Songs</button>
            <ul>
                {songs.map((song, index) => <li key={index}>{song}</li>)}
            </ul>
        </div>
    );
}

export default Playlist;
