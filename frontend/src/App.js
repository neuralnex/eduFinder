import React from 'react';
import './App.css';

function App() {
  const agents = {
    status: "EduFinder Multi-Agent System Running",
    message: "Welcome to EduFinder! Your AI-powered learning companion.",
    agents: {
      main_agent: "agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne",
      curriculum_agent: "agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8",
      materials_agent: "agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf",
      enhanced_agent: "agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4"
    },
    ports: {
      main_agent: 8000,
      curriculum_agent: 8001,
      materials_agent: 8002,
      enhanced_agent: 8003
    },
    profile_links: {
      main_agent: "https://agentverse.ai/agents/details/agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne/profile",
      curriculum_agent: "https://agentverse.ai/agents/details/agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8/profile",
      materials_agent: "https://agentverse.ai/agents/details/agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf/profile",
      enhanced_agent: "https://agentverse.ai/agents/details/agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4/profile"
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚀 EduFinder</h1>
        <p className="subtitle">AI-Powered Learning Path System</p>
        <p className="status">{agents?.status}</p>
        <p className="message">{agents?.message}</p>
      </header>

      <main className="app-main">
        <section className="agents-section">
          <h2>🤖 Active Agents</h2>
          <div className="agents-grid">
            {agents?.agents && Object.entries(agents.agents).map(([key, address]) => {
              const imageMap = {
                'main_agent': 'learningpath.jpeg',
                'curriculum_agent': 'curriculum.jpeg',
                'materials_agent': 'materials.jpeg',
                'enhanced_agent': 'enhanced.jpeg'
              };
              
              return (
                <div key={key} className="agent-card">
                  <a 
                    href={agents.profile_links[key]} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="agent-image-link"
                  >
                    <img 
                      src={`/images/${imageMap[key]}`} 
                      alt={`${key.replace('_', ' ')} Agent`}
                      className="agent-image"
                    />
                  </a>
                  <h3>{key.replace('_', ' ').toUpperCase()}</h3>
                  <p className="address">{address}</p>
                  <a 
                    href={agents.profile_links[key]} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="profile-link"
                  >
                    View Profile →
                  </a>
                </div>
              );
            })}
          </div>
        </section>

        <section className="ports-section">
          <h2>🔌 Agent Ports</h2>
          <div className="ports-grid">
            {agents?.ports && Object.entries(agents.ports).map(([key, port]) => (
              <div key={key} className="port-card">
                <h3>{key.replace('_', ' ').toUpperCase()}</h3>
                <p className="port">Port: {port}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="actions-section">
          <h2>🎯 Quick Actions</h2>
          <div className="actions-grid">
            <button className="action-btn primary">
              📚 Start Learning
            </button>
            <button className="action-btn secondary">
              🔍 Find Resources
            </button>
            <button className="action-btn tertiary">
              🧠 Get Insights
            </button>
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <p>Powered by uAgents Framework & Gemini AI</p>
        <div className="footer-links">
          <a href="https://agentverse.ai" target="_blank" rel="noopener noreferrer">
            AgentVerse
          </a>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
        </div>
      </footer>
    </div>
  );
}

export default App;
