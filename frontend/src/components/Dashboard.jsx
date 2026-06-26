export default function Dashboard({ stats }) {
    const handleDownloadReport = () => {
        const reportText = `IoT Scanner Report\nTotal Scans: ${stats.scans}\nCritical Alerts: ${stats.critical_alerts}\nHigh Alerts: ${stats.high_alerts}\n`;
        const blob = new Blob([reportText], {type: 'text/plain'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'iot_security_report.txt';
        a.click();
    };

    return (
        <div>
            <div className="title" style={{ justifyContent: 'space-between' }}>
                System Overview
                <button onClick={handleDownloadReport} className="primary" style={{ fontSize: '0.9rem' }}>Download Report</button>
            </div>
            <div className="grid">
                <div className="stat-box">
                    <div className="num">{stats.scans}</div>
                    <div className="label">Ports Scanned Total</div>
                </div>
                <div className="stat-box" style={{ borderColor: 'var(--danger)' }}>
                    <div className="num" style={{ color: 'var(--danger)' }}>{stats.critical_alerts}</div>
                    <div className="label">Critical Vulnerabilities</div>
                </div>
                <div className="stat-box" style={{ borderColor: 'var(--warning)' }}>
                    <div className="num" style={{ color: 'var(--warning)' }}>{stats.high_alerts}</div>
                    <div className="label">High Risk Warnings</div>
                </div>
            </div>
            
            <div className="card">
                <div className="title">IoT Scanner Engine Status</div>
                <p style={{ display: 'flex', alignItems: 'center' }}>
                    <span className="live-indicator"></span> 
                    Virtual IoT Background Service is operational.
                </p>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    Scans are executed automatically every 60 seconds against localhost. Security data is ingested into the local SQLite database. Ensure both <code>main.py</code> API server and <code>background_service.py</code> are running.
                </p>
            </div>
        </div>
    );
}
