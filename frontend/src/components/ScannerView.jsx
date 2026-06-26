import { useState, useEffect } from 'react';

export default function ScannerView() {
    const [scans, setScans] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchScans = async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/scan');
            if (res.ok) {
                const data = await res.json();
                setScans(data.scans);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchScans();
        const int = setInterval(fetchScans, 5000);
        return () => clearInterval(int);
    }, []);

    return (
        <div className="card">
            <div className="title">Live Scan Results</div>
            
            {loading && <p>Loading scan data...</p>}
            
            {!loading && scans.length === 0 && (
                <p style={{ color: 'var(--text-muted)' }}>No scans recorded yet. Waiting for virtual IoT device...</p>
            )}

            {!loading && scans.length > 0 && (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Target</th>
                            <th>Port</th>
                            <th>Service</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {scans.map((scan) => (
                            <tr key={scan.id}>
                                <td>{new Date(scan.scanned_at).toLocaleTimeString()}</td>
                                <td>{scan.target_ip}</td>
                                <td><strong>{scan.port}</strong></td>
                                <td>{scan.service || 'Unknown'}</td>
                                <td><span className="badge low">{scan.status}</span></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
