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
          </div>
          <div className="header-actions">
            <a 
              href="https://github.com/neuralnex/eduFinder" 
              target="_blank" 
              rel="noopener noreferrer"
              className="github-link"
              title="View on GitHub"
            >
              <svg className="github-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </a>
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

      <section className="elevator-pitch-section">
        <div className="elevator-pitch-container">
          <h2 className="pitch-hook">🎯 Stop Wasting Time on Random Tutorials!</h2>
          <p className="elevator-pitch">
            <strong>EduFinder is the world's first AI-powered learning orchestrator</strong> that creates personalized educational journeys for ANY domain. 
            Whether you want to master Python, learn quantum physics, or become a professional chef - our advanced MeTTa Knowledge Graph 
            and Gemini AI work together to map your exact learning path, discover the perfect resources, and accelerate your mastery 
            with unprecedented precision. <span className="highlight">No more guesswork. No more wasted time. Just pure, intelligent learning.</span>
          </p>
          <div className="pitch-stats">
            <div className="stat-item">
              <span className="stat-number">∞</span>
              <span className="stat-label">Domains Supported</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">⚡</span>
              <span className="stat-label">Real-time AI</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">🧠</span>
              <span className="stat-label">Smart Prerequisites</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">🎯</span>
              <span className="stat-label">Personalized Paths</span>
            </div>
          </div>
        </div>
      </section>

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
                  <h3>{key === 'main_agent' ? 'LEARNINGPATH' : key.replace('_', ' ').toUpperCase()}</h3>
                  
                  <div className="agent-description">
                    {key === 'main_agent' && (
                      <p><strong>Powerful Learning Orchestrator:</strong> Advanced AI routing system that intelligently coordinates all learning requests, analyzes complex queries, and directs you to the most effective learning resources with unprecedented precision.</p>
                    )}
                    {key === 'curriculum_agent' && (
                      <p><strong>Master Curriculum Architect:</strong> Harnesses cutting-edge AI to craft highly personalized, structured learning paths and comprehensive educational curricula perfectly tailored to your unique goals, skill level, and learning style.</p>
                    )}
                    {key === 'materials_agent' && (
                      <p><strong>Supreme Resource Discovery Engine:</strong> Leverages powerful AI algorithms to discover, curate, and recommend the finest learning resources including premium videos, courses, documentation, and hands-on projects from across the web.</p>
                    )}
                    {key === 'enhanced_agent' && (
                      <p><strong>Deep Learning Intelligence:</strong> Provides profound insights, advanced concept analysis, and comprehensive learning dependency mapping to dramatically accelerate your understanding and mastery of complex topics.</p>
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

      </main>

      <footer className="app-footer">
        <div className="tech-stack">
          <h3>🚀 Technology Stack</h3>
          <div className="tech-grid">
            <div className="tech-category">
              <h4>AI & Machine Learning</h4>
              <ul>
                <li>Google Gemini AI</li>
                <li>MeTTa Knowledge Graph</li>
                <li>Advanced NLP Processing</li>
                <li>Intelligent Query Analysis</li>
                <li>Personalized Learning Algorithms</li>
              </ul>
            </div>
            <div className="tech-category">
              <h4>Agent Framework</h4>
              <ul>
                <li>uAgents Framework</li>
                <li>Multi-Agent Architecture</li>
                <li>Real-time Communication</li>
                <li>Distributed Processing</li>
              </ul>
            </div>
            <div className="tech-category">
              <h4>Frontend & UI</h4>
              <ul>
                <li>React.js</li>
                <li>Modern CSS3</li>
                <li>Responsive Design</li>
                <li>Interactive Components</li>
              </ul>
            </div>
            <div className="tech-category">
              <h4>Backend & Infrastructure</h4>
              <ul>
                <li>Python FastAPI</li>
                <li>AgentVerse Platform</li>
                <li>Cloud Infrastructure</li>
                <li>Scalable Architecture</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>Powered by uAgents Framework & Gemini AI | Built with cutting-edge technology for the future of education</p>
          <div className="footer-links">
            <a href="https://agentverse.ai" target="_blank" rel="noopener noreferrer">
              AgentVerse
            </a>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
            <a href="https://ai.google.dev/gemini-api" target="_blank" rel="noopener noreferrer">
              Gemini AI
            </a>
            <a href="https://metta-lang.dev" target="_blank" rel="noopener noreferrer">
              MeTTa Lang
            </a>
            <a href="https://uagents.readthedocs.io" target="_blank" rel="noopener noreferrer">
              uAgents Docs
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
