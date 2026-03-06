import React, { useState } from 'react';
import { motion } from 'framer-motion';

const CodeInput = ({ onAnalyze, isLoading }) => {
    const [code, setCode] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (code.trim()) {
            onAnalyze(code);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card mb-4"
        >
            <h3 className="mb-3 text-white">Source Code Analysis</h3>
            <form onSubmit={handleSubmit}>
                <textarea
                    className="form-control mb-3"
                    rows="12"
                    placeholder="Paste your C, C++, Java, or Python code here..."
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    spellCheck="false"
                ></textarea>
                <div className="d-flex justify-content-end">
                    <button
                        type="submit"
                        className="btn btn-primary-custom"
                        disabled={isLoading || !code.trim()}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                Analyzing...
                            </>
                        ) : (
                            'Analyze Code'
                        )}
                    </button>
                </div>
            </form>
        </motion.div>
    );
};

export default CodeInput;
