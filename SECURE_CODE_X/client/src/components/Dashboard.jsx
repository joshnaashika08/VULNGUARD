import React, { useState } from 'react';
import axios from 'axios';
import CodeInput from './CodeInput';
import Results from './Results';

const Dashboard = () => {
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleAnalyze = async (code) => {
        setIsLoading(true);
        setError(null);
        setResults(null);

        try {
            // In development, Vite proxies /analyze to 5000. 
            // If running separately, ensures CORS is handled on backend.
            const response = await axios.post('http://localhost:5000/analyze', { code });
            setResults(response.data);
        } catch (err) {
            console.error(err);
            setError("Analysis failed. Ensure the backend server is running.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="text-center mb-5">
                <h1 className="display-4 fw-bold text-gradient" style={{
                    background: 'linear-gradient(to right, #38bdf8, #818cf8)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                }}>
                    AI Vulnerability Analyzer
                </h1>
                <p className="lead text-secondary">
                    Detect security flaws in C, C++, Java, and Python with advanced static analysis.
                </p>
            </div>

            <div className="row justify-content-center">
                <div className="col-lg-10">
                    <CodeInput onAnalyze={handleAnalyze} isLoading={isLoading} />

                    {error && (
                        <div className="alert alert-danger mt-3 glass-card text-white">
                            {error}
                        </div>
                    )}

                    <Results results={results} />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
