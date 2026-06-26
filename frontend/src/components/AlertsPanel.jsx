import { useState, useEffect } from 'react';

export default function AlertsPanel() {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchAlerts = async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/alerts');
            if (res.ok) {
                const data = await res.json();
                setAlerts(data.alerts);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAlerts();
        const int = setInterval(fetchAlerts, 5000);
        return () => clearInterval(int);
    }, []);

    return (
        <div className="card">
            <div className="title">Security Alerts</div>
            
            {loading && <p>Loading alerts...</p>}
            
            {!loading && alerts.length === 0 && (
                <p style={{ color: 'var(--text-muted)' }}>No alerts at this time. System is secure.</p>
            )}

            {!loading && alerts.length > 0 && (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Severity</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {alerts.map((alert) => (
                            <tr key={alert.id}>
                                <td>{new Date(alert.created_at).toLocaleTimeString()}</td>
                                <td>
                                    <span className={`badge ${alert.severity.toLowerCase()}`}>
                                        {alert.severity}
                                    </span>
                                </td>
                                <td>{alert.message}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
