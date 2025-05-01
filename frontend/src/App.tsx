import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CandidateUpload from './components/CandidateUpload';
import Header from './components/Header';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<CandidateUpload />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;