// src/App.jsx - Entry point with dashboard

import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>Portfolio App</h1>
      <Dashboard />
    </div>
  );
}

export default App;