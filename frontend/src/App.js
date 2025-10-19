import React, { useState, useMemo } from 'react';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const agents = {
    status: "EduFinder Multi-Agent System Running",
    message: "Welcome to EduFinder! Your AI-powered learning companion.",
    agents: {
      main_agent: "agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne",
      curriculum_agent: "agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8",
      materials_agent: "agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf",
      enhanced_agent: "agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4"
    },
    profile_links: {
      main_agent: "https://agentverse.ai/agents/details/agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne/profile",
      curriculum_agent: "https://agentverse.ai/agents/details/agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8/profile",
      materials_agent: "https://agentverse.ai/agents/details/agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf/profile",
      enhanced_agent: "https://agentverse.ai/agents/details/agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4/profile"
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Agent address copied to clipboard!');
    });
  };

  const filteredAgents = useMemo(() => {
    const agentEntries = Object.entries(agents.agents);
    
    return agentEntries.filter(([key, address]) => {
      const agentName = key.replace('_', ' ').toLowerCase();
      const matchesSearch = agentName.includes(searchTerm.toLowerCase()) || 
                           address.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesFilter = filterType === 'all' || 
                           (filterType === 'learning' && key === 'main_agent') ||
                           (filterType === 'curriculum' && key === 'curriculum_agent') ||
                           (filterType === 'materials' && key === 'materials_agent') ||
                           (filterType === 'insights' && key === 'enhanced_agent');
      
      return matchesSearch && matchesFilter;
    });
  }, [searchTerm, filterType, agents.agents]);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <img src="/images/logo.svg" alt="EduFinder Logo" className="logo" />
          </div>
          <div className="header-text">
            <h1>🚀 EduFinder</h1>
            <p className="elevator-pitch">
              Transform your learning journey with AI-powered educational agents. 
              Get personalized curricula, discover resources, and gain deep insights 
              across any technical domain - all powered by cutting-edge AI technology.
            </p>
          </div>
          <div className="header-actions">
            <a 
              href="http://asi1.ai/chat" 
              target="_blank" 
              rel="noopener noreferrer"
              className="chat-link"
            >
              💬 ASI1 Chat
            </a>
          </div>
        </div>
      </header>

      <main className="app-main">
        <section className="search-section">
          <div className="search-container">
            <div className="search-box">
              <input
                type="text"
                placeholder="Search agents by name or address..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <span className="search-icon">🔍</span>
            </div>
            
            <div className="filter-container">
              <label className="filter-label">Filter by type:</label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="filter-select"
              >
                <option value="all">All Agents</option>
                <option value="learning">Learning Path</option>
                <option value="curriculum">Curriculum</option>
                <option value="materials">Materials</option>
                <option value="insights">Insights</option>
              </select>
            </div>
          </div>
          
          <div className="search-results">
            <p className="results-count">
              Showing {filteredAgents.length} of {Object.keys(agents.agents).length} agents
            </p>
          </div>
        </section>

        <section className="agents-section">
          <h2>🤖 Active Agents</h2>
          <div className="agents-grid">
            {filteredAgents.map(([key, address]) => {
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
                  
                  <div className="agent-description">
                    {key === 'main_agent' && (
                      <p>Main routing agent that coordinates all learning requests and provides intelligent query analysis.</p>
                    )}
                    {key === 'curriculum_agent' && (
                      <p>Creates structured learning paths and educational curricula tailored to your specific goals and skill level.</p>
                    )}
                    {key === 'materials_agent' && (
                      <p>Discovers and curates learning resources including videos, courses, documentation, and hands-on projects.</p>
                    )}
                    {key === 'enhanced_agent' && (
                      <p>Provides deep insights, concept analysis, and learning dependencies to accelerate your understanding.</p>
                    )}
                  </div>
                  
                  <div className="agent-features">
                    <div className="feature-tag">🤖 AI-Powered</div>
                    <div className="feature-tag">🔗 AgentVerse</div>
                    <div className="feature-tag">⚡ Real-time</div>
                  </div>
                  
                  <div className="address-container">
                    <p className="address">{address}</p>
                    <button 
                      onClick={() => copyToClipboard(address)}
                      className="copy-btn"
                      title="Copy address"
                    >
                      📋
                    </button>
                  </div>
                  
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
