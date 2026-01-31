import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import { 
  Terminal, 
  Zap, 
  Shield, 
  Activity,
  Play,
  Square,
  Trash2,
  Download,
  Settings,
  Globe,
  Server,
  Code,
  FileText,
  Target
} from 'lucide-react';

const GATEWAY_URL = 'http://localhost:18789';

function App() {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [objective, setObjective] = useState('');
  const [logs, setLogs] = useState([]);
  const [missionActive, setMissionActive] = useState(false);
  const [stats, setStats] = useState({ missions: 0, findings: 0, errors: 0, uptime: 0 });
  const terminalRef = useRef(null);

  useEffect(() => {
    const newSocket = io(GATEWAY_URL, {
      transports: ['websocket', 'polling']
    });

    newSocket.on('connect', () => {
      setConnected(true);
      addLog('system', 'Neural link established. STINGBOT online.');
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      addLog('error', 'Neural link disconnected.');
    });

    newSocket.on('neural:update', (data) => {
      addLog('info', data.log || data.status);
    });

    newSocket.on('neural:log', (data) => {
      addLog('info', data.message);
    });

    newSocket.on('neural:error', (data) => {
      addLog('error', data.error);
    });

    newSocket.on('neural:complete', (data) => {
      addLog('success', `Mission Result: ${data.result}`);
      setMissionActive(false);
      setStats(prev => ({ ...prev, missions: prev.missions + 1 }));
    });

    newSocket.on('mission:complete', (data) => {
      if (data.success) {
        addLog('success', 'Mission completed successfully.');
      } else {
        addLog('error', `Mission failed: ${data.error}`);
        setStats(prev => ({ ...prev, errors: prev.errors + 1 }));
      }
      setMissionActive(false);
    });

    newSocket.on('command:output', (data) => {
      addLog(data.isError ? 'error' : 'info', data.chunk);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs]);

  const addLog = (type, message) => {
    const timestamp = new Date().toLocaleTimeString('en-US', { hour12: false });
    setLogs(prev => [...prev.slice(-200), { type, message, timestamp }]);
  };

  const startMission = () => {
    if (!objective.trim() || !socket) return;
    
    addLog('system', `Initiating mission: ${objective}`);
    socket.emit('mission:start', { objective: objective.trim() });
    setMissionActive(true);
    setObjective('');
  };

  const abortMission = () => {
    if (socket) {
      socket.emit('mission:abort');
      addLog('warning', 'Mission abort requested.');
      setMissionActive(false);
    }
  };

  const clearLogs = () => {
    setLogs([]);
    addLog('system', 'Terminal cleared.');
  };

  const exportLogs = () => {
    const logText = logs.map(l => `[${l.timestamp}] ${l.type.toUpperCase()}: ${l.message}`).join('\n');
    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `stingbot-logs-${Date.now()}.txt`;
    a.click();
  };

  const quickAction = (action) => {
    const actions = {
      'scan-local': 'Perform a network scan on localhost',
      'system-info': 'Get system information and security posture',
      'vuln-check': 'Check for common vulnerabilities on the local network',
    };
    if (actions[action]) {
      setObjective(actions[action]);
    }
  };

  const getLogIcon = (type) => {
    switch (type) {
      case 'success': return '✓';
      case 'error': return '✘';
      case 'warning': return '!';
      case 'system': return '◆';
      default: return '→';
    }
  };

  const agents = [
    { name: 'Web Pentester', type: 'OFFENSIVE', active: missionActive },
    { name: 'Net Pentester', type: 'RECON', active: false },
    { name: 'Rev Engineer', type: 'ANALYSIS', active: false },
    { name: 'Critic', type: 'REVIEW', active: false },
    { name: 'Reporter', type: 'OUTPUT', active: false },
  ];

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">🦂</div>
          <span className="logo-text">STINGBOT</span>
        </div>
        <div className="status-indicator">
          <span className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></span>
          <span>{connected ? 'Neural Link Active' : 'Disconnected'}</span>
        </div>
      </header>

      <main className="main">
        <section className="terminal-section">
          <div className="mission-input">
            <h2><Target size={18} /> Mission Objective</h2>
            <div className="input-group">
              <input
                type="text"
                value={objective}
                onChange={(e) => setObjective(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !missionActive && startMission()}
                placeholder="Enter objective (e.g., 'Scan 192.168.1.1 for vulnerabilities')"
                disabled={missionActive}
              />
              {!missionActive ? (
                <button 
                  className="btn btn-primary" 
                  onClick={startMission}
                  disabled={!connected || !objective.trim()}
                >
                  <Play size={18} /> Execute
                </button>
              ) : (
                <button className="btn btn-danger" onClick={abortMission}>
                  <Square size={18} /> Abort
                </button>
              )}
            </div>
          </div>

          <div className="terminal">
            <div className="terminal-header">
              <div className="terminal-title">
                <Terminal size={16} />
                <span>Neural Output Stream</span>
              </div>
              <div className="terminal-controls">
                <span className="terminal-dot red"></span>
                <span className="terminal-dot yellow"></span>
                <span className="terminal-dot green"></span>
              </div>
            </div>
            <div className="terminal-body" ref={terminalRef}>
              {logs.length === 0 ? (
                <div className="log-entry system">
                  <span className="log-icon">◆</span>
                  <span className="log-message">STINGBOT v2.0 initialized. Awaiting mission objective...</span>
                </div>
              ) : (
                logs.map((log, index) => (
                  <div key={index} className={`log-entry ${log.type}`}>
                    <span className="log-time">{log.timestamp}</span>
                    <span className="log-icon">{getLogIcon(log.type)}</span>
                    <span className="log-message">{log.message}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>

        <aside className="sidebar">
          <div className="panel">
            <h3>Mission Stats</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-value">{stats.missions}</div>
                <div className="stat-label">Missions</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{stats.findings}</div>
                <div className="stat-label">Findings</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{stats.errors}</div>
                <div className="stat-label">Errors</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{connected ? 'ON' : 'OFF'}</div>
                <div className="stat-label">Status</div>
              </div>
            </div>
          </div>

          <div className="panel">
            <h3>Active Agents</h3>
            <div className="agent-list">
              {agents.map((agent, index) => (
                <div key={index} className="agent-item">
                  <span className={`agent-status ${agent.active ? 'active' : ''}`}></span>
                  <span className="agent-name">{agent.name}</span>
                  <span className="agent-type">{agent.type}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="panel">
            <h3>Quick Actions</h3>
            <div className="quick-actions">
              <button className="action-btn" onClick={() => quickAction('scan-local')}>
                <Globe size={18} />
                <span>Scan Local Network</span>
              </button>
              <button className="action-btn" onClick={() => quickAction('system-info')}>
                <Server size={18} />
                <span>System Analysis</span>
              </button>
              <button className="action-btn" onClick={() => quickAction('vuln-check')}>
                <Shield size={18} />
                <span>Vulnerability Check</span>
              </button>
              <button className="action-btn" onClick={clearLogs}>
                <Trash2 size={18} />
                <span>Clear Terminal</span>
              </button>
              <button className="action-btn" onClick={exportLogs}>
                <Download size={18} />
                <span>Export Logs</span>
              </button>
            </div>
          </div>
        </aside>
      </main>

      <footer className="footer">
        <span>STINGBOT v2.0 | Multi-Agent Security System</span>
        <span>Gateway: {GATEWAY_URL}</span>
      </footer>
    </div>
  );
}

export default App;
