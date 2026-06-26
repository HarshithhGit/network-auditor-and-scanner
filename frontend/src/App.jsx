import { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import ScannerView from './components/ScannerView';
import PasswordAuditor from './components/PasswordAuditor';
import AlertsPanel from './components/AlertsPanel';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState({ scans: 0, critical_alerts: 0, high_alerts: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/stats');
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (e) {
        console.error("Could not fetch stats, backend might be offline.");
      }
    };
    fetchStats();
    const int = setInterval(fetchStats, 5000);
    return () => clearInterval(int);
  }, []);

  return (
    <div>
      <div className="header">
        <h1>IoT Security Scanner</h1>
        <div style={{display: 'flex', gap: '12px'}}>
          <button className={activeTab === 'dashboard' ? 'primary' : ''} onClick={() => setActiveTab('dashboard')}>Dashboard</button>
          <button className={activeTab === 'scanner' ? 'primary' : ''} onClick={() => setActiveTab('scanner')}>Live Scanner</button>
          <button className={activeTab === 'password' ? 'primary' : ''} onClick={() => setActiveTab('password')}>Password Auditor</button>
          <button className={activeTab === 'alerts' ? 'primary' : ''} onClick={() => setActiveTab('alerts')}>
            Alerts {stats.critical_alerts > 0 && <span className="badge critical" style={{marginLeft: '8px'}}>{stats.critical_alerts}</span>}
          </button>
        </div>
      </div>
      
      <div className="main-content">
        {activeTab === 'dashboard' && <Dashboard stats={stats} />}
        {activeTab === 'scanner' && <ScannerView />}
        {activeTab === 'password' && <PasswordAuditor />}
        {activeTab === 'alerts' && <AlertsPanel />}
      </div>
    </div>
  );
}

export default App;
