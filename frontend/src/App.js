// ALL IMPORTS AT THE TOP
import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import './App.css'; 

// All other code (functions, components) comes AFTER
const AnalysisPage = () => <h2>Analysis Page (Placeholder)</h2>;

function App() {
  return (
    <BrowserRouter>
      {/* You could add a Nav bar here */}
      <nav style={{ padding: '10px', background: '#eee' }}>
        <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
        <Link to="/analysis">Analysis</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;