import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ScoreCard = ({ title, score, color }) => (
    <div className="text-center p-3">
        <div className="score-circle mb-2" style={{ borderColor: color, color: color }}>
            {score}
        </div>
        <h5 className="mt-3 text-light font-bold" style={{ letterSpacing: '1px' }}>{title}</h5>
    </div>
);

const Results = ({ results }) => {
    if (!results) return null;

    const { language, vulnerabilities, code_quality_score, security_score, overall_confidence } = results;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4"
        >
            {/* Scores Section */}
            <div className="glass-card mb-4">
                <div className="row justify-content-center">
                    <div className="col-md-4">
                        <ScoreCard title="Risk Score" score={security_score} color={parseInt(security_score) > 70 ? '#22c55e' : parseInt(security_score) > 40 ? '#f59e0b' : '#ef4444'} />
                    </div>
                    <div className="col-md-4">
                        <ScoreCard title="Quality Score" score={code_quality_score} color="#38bdf8" />
                    </div>
                    <div className="col-md-4">
                        <div className="text-center p-3">
                            <h2 className="mb-0 text-white">{overall_confidence}</h2>
                            <p className="text-muted">Confidence</p>
                            <div className="badge bg-secondary text-uppercase mt-2">{language} Detected</div>
                        </div>
                    </div>
                </div>

                <div className="d-flex justify-content-end mb-3">
                    <button
                        className="btn btn-outline-light"
                        onClick={async () => {
                            try {
                                const response = await fetch('http://localhost:5000/report/pdf', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify(results)
                                });
                                const blob = await response.blob();
                                const url = window.URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'vulnerability_report.pdf';
                                a.click();
                            } catch (e) {
                                console.error("PDF Download failed", e);
                                alert("Failed to download PDF");
                            }
                        }}
                    >
                        Download PDF Report
                    </button>
                </div>
            </div>

            {/* Vulnerabilities List */}
            <h3 className="mb-3 text-white">Detected Vulnerabilities ({vulnerabilities.length})</h3>

            <AnimatePresence>
                {vulnerabilities.length === 0 ? (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="alert alert-success glass-card"
                    >
                        Type: Secure. No vulnerabilities detected.
                    </motion.div>
                ) : (
                    vulnerabilities.map((vuln, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className={`card vuln-card vuln-${vuln.severity} p-3 mb-3 text-white`}
                        >
                            <div className="d-flex justify-content-between align-items-start">
                                <div>
                                    <h5 className="mb-1">
                                        {vuln.type}
                                        <span className={`badge ms-2 bg-${vuln.severity === 'Critical' ? 'danger' : vuln.severity === 'High' ? 'danger' : vuln.severity === 'Medium' ? 'warning' : 'success'}`}>
                                            {vuln.severity}
                                        </span>
                                    </h5>
                                    <p className="mb-1 text-muted">Line {vuln.line}: {vuln.description}</p>
                                </div>
                                <div className="text-end text-muted small">
                                    Confidence: {vuln.confidence}
                                </div>
                            </div>

                            <div className="mt-2 p-2 rounded" style={{ background: 'rgba(0,0,0,0.2)' }}>
                                <strong>Fix:</strong> <span className="text-info">{vuln.suggested_fix}</span>
                            </div>
                        </motion.div>
                    ))
                )}
            </AnimatePresence>
        </motion.div>
    );
};

export default Results;
