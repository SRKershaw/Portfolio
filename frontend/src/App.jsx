// src/App.jsx - Full-stack "Hello World": fetches from backend

import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    // Fetch from backend API
    fetch('http://localhost:8000/')
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage(`Error: ${err.message}`));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>Portfolio App</h1>
      <p><strong>Backend says:</strong> {message}</p>
    </div>
  );
}

export default App;