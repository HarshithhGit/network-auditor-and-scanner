import { useState, useEffect } from 'react';

export default function PasswordAuditor() {
    const [password, setPassword] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const checkPassword = async () => {
            if (!password) {
                setResult(null);
                return;
            }
            
            setLoading(true);
            try {
                const res = await fetch('http://127.0.0.1:8000/api/password-check', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password })
                });
                
                if (res.ok) {
                    const data = await res.json();
                    setResult(data);
                }
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };

        const timeout = setTimeout(() => {
            checkPassword();
        }, 300); // 300ms debounce
        
        return () => clearTimeout(timeout);
    }, [password]);

    return (
        <div>
            <div className="card">
                <div className="title">Password Auditor</div>
                <p style={{ marginBottom: '20px', color: 'var(--text-muted)' }}>
                    Type a password below to analyze its strength, calculate entropy, and estimate the time it would take to crack using a brute force attack.
                </p>
                
                <input 
                    type="text" 
                    placeholder="Enter password..." 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ marginBottom: '20px', fontSize: '1.2rem' }}
                />

                {loading && <p>Analyzing...</p>}
                
                {result && !loading && (
                    <div>
                        <div style={{ marginBottom: '20px', background: '#010409', padding: '16px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                                <strong>Score: {result.score}/100</strong>
                                <span className={`badge ${result.risk.toLowerCase()}`}>
                                    Risk: {result.risk}
                                </span>
                            </div>
                            
                            {/* Progress bar */}
                            <div style={{ width: '100%', height: '8px', background: 'var(--border)', borderRadius: '4px', overflow: 'hidden' }}>
                                <div style={{ 
                                    width: `${result.score}%`, 
                                    height: '100%', 
                                    background: result.score > 80 ? 'var(--success)' : result.score > 40 ? 'var(--warning)' : 'var(--danger)',
                                    transition: 'width 0.3s ease'
                                }}></div>
                            </div>
                            
                            <p style={{ marginTop: '16px', fontSize: '0.95rem' }}>{result.feedback}</p>
                        </div>
                        
                        <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
                            <div className="stat-box">
                                <div className="num" style={{ fontSize: '1.8rem' }}>{result.crack_time}</div>
                                <div className="label">Est. Crack Time</div>
                            </div>
                            <div className="stat-box">
                                <div className="num" style={{ fontSize: '1.8rem' }}>{result.entropy}</div>
                                <div className="label">Entropy Bits</div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
