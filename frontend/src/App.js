// ALL IMPORTS AT THE TOP
import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import AnalysisPage from './components/AnalysisPage';
import './App.css'; 

function App() {
  return (
    <BrowserRouter>
      {/* You could add a Nav bar here */}
      <nav style={{ padding: '10px', background: '#eee' }}>
        <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/analysis/:eventId" element={<AnalysisPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;