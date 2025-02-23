import React from 'react';
import { createRoot } from 'react-dom/client'; // ✅ Ensure correct import
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// ✅ Fix: Correct usage of createRoot
const root = createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

