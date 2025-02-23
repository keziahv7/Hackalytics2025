import React, { useEffect } from 'react';
import './DinoGame.css';

function Gamification() {
    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/gh/wayou/t-rex-runner@gh-pages/trex.js';
        script.async = true;
        document.body.appendChild(script);
    }, []);

    return (
        <div className="dino-game-container">
            <h2>Play the Dino Game!</h2>
            <canvas id="canvas" width="600" height="150"></canvas>
            <p>Press **Spacebar** to jump!</p>
        </div>
    );
}

export default Gamification;
