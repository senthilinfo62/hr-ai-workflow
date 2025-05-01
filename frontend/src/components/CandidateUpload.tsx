import React, { useState } from 'react';
import axios from 'axios';

interface CandidateResult {
  name: string;
  email: string;
  phone: string;
  city: string;
  education: string;
  job_history: string;
  skills: string[];
  score: number;
}

const CandidateUpload: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CandidateResult | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || !email || !file) {
      setError('Please fill all fields');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('cv', file);

    try {
      const response = await axios.post('http://localhost:8000/api/cv/candidates', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('Error processing CV. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="candidate-upload">
      <h2>Upload Candidate CV</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="cv">CV (PDF)</label>
          <input
            type="file"
            id="cv"
            accept=".pdf"
            onChange={e => setFile(e.target.files?.[0] || null)}
            required
          />
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Upload and Process'}
        </button>
      </form>

      {result && (
        <div className="result">
          <h3>Results</h3>
          <div className="result-card">
            <h4>{result.name}</h4>
            <p>
              <strong>Email:</strong> {result.email}
            </p>
            <p>
              <strong>Phone:</strong> {result.phone}
            </p>
            <p>
              <strong>City:</strong> {result.city}
            </p>

            <div className="section">
              <h5>Education</h5>
              <p>{result.education}</p>
            </div>

            <div className="section">
              <h5>Job History</h5>
              <p>{result.job_history}</p>
            </div>

            <div className="section">
              <h5>Skills</h5>
              <ul>
                {result.skills.map((skill: string, index: number) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </div>

            <div className="section">
              <h5>Score</h5>
              <p>{result.score}/10</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CandidateUpload;
