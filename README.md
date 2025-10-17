![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# 🚀 EduFinder - AI-Powered Learning Path System

**EduFinder** is an intelligent multi-agent system that creates personalized educational plans, discovers targeted learning resources, and provides deep insights for any technical domain. Built with **uAgents** framework and powered by **Gemini AI** and **MeTTa Knowledge Graph**.

## ✨ Key Features

### 🎯 **Smart Query Understanding**
- **Context-Aware Responses**: Gemini AI analyzes each specific query
- **Personalized Learning Plans**: Tailored to user's exact needs
- **Dynamic Domain Support**: Handles any educational or technical domain
- **Intelligent Routing**: Automatically routes requests to specialized agents

### 📚 **Comprehensive Educational Plans**
- **Step-by-Step Learning Paths**: Clear progression from beginner to advanced
- **Integrated Resources**: Direct links to courses, documentation, and tutorials
- **YouTube Integration**: Real-time educational video discovery
- **Project-Based Learning**: Hands-on exercises and practical applications

### 🧠 **Deep Insights & Analysis**
- **Concept Relationships**: Understand how topics connect and relate
- **Prerequisite Mapping**: Know what you need to learn first
- **Learning Dependencies**: Optimal order for mastering concepts
- **Cross-Domain Connections**: Show relationships across different fields

## 🏗️ System Architecture

### **Multi-Agent Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                    Main Learning Path Agent                  │
│                     (Port 8000)                             │
│  • Smart Query Analysis & Routing                           │
│  • Inter-Agent Communication                               │
│  • Response Coordination & Forwarding                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Curriculum  │ │ Materials   │ │ Enhanced    │
│ Agent       │ │ Agent       │ │ Agent       │
│ (Port 8001) │ │ (Port 8002) │ │ (Port 8003) │
│             │ │             │ │             │
│ • Educational│ │ • Resource  │ │ • Deep      │
│   Plans      │ │   Discovery │ │   Insights  │
│ • Step-by-   │ │ • YouTube   │ │ • Concept   │
│   Step       │ │   Videos    │ │   Analysis  │
│   Resources  │ │ • Courses   │ │ • Learning  │
│             │ │ • Tutorials │ │   Dependencies│
└─────────────┘ └─────────────┘ └─────────────┘
```

### **Technology Stack**
- **🤖 uAgents Framework**: Autonomous AI agent communication
- **🧠 Gemini AI**: Google's AI for content generation and analysis
- **📊 MeTTa Knowledge Graph**: Structured learning concept relationships
- **🎥 YouTube API**: Real-time educational video discovery
- **🐍 Python 3.8+**: Core application language

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- API Keys: Gemini AI, YouTube (optional)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/neuralnex/eduFinder.git
cd eduFinder

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### **Environment Variables**
```bash
# Agent Configuration
AGENT_SEED=your_main_agent_seed
AGENT_NAME=LearningPathAgent
AGENT_DESCRIPTION=An AI agent that creates personalized learning curricula

# Agent Seeds (for specialized agents)
CURRICULUM_AGENT_SEED=curriculum
MATERIALS_AGENT_SEED=materials
ENHANCED_AGENT_SEED=enhanced

# API Keys
GEMINI_API_KEY=your_gemini_api_key  # Get from: https://aistudio.google.com/app/apikey
YOUTUBE_API_KEY=your_youtube_api_key  # Get from: https://console.developers.google.com/apis/credentials

# MeTTa Configuration
METTA_ENDPOINT=http://localhost:8080
METTA_SPACE=learning_space
METTA_USE_MOCK=false

# AgentVerse Configuration
AGENTVERSE_ENDPOINT=https://agentverse.ai
FETCH_ENDPOINT=https://fetch.ai

# Debug Settings
DEBUG=True
LOG_LEVEL=INFO
```

### **Running the System**
```bash
# Start all agents in different terminals
python3 agents/curriculum_agent.py &
python3 agents/materials_agent.py &
python3 agents/enhanced_agent.py &
python3 agent.py
```

## 💬 Usage Examples

### **Educational Plan Creation**
```
User: "Teach me Python for data science"
Response: Comprehensive Python curriculum focused on pandas, numpy, matplotlib, 
          Jupyter notebooks, statistical analysis, and data visualization
```

### **Resource Discovery**
```
User: "Find React tutorials for beginners"
Response: Targeted beginner-friendly React resources, courses, documentation, 
          and YouTube videos with direct links
```

### **Deep Insights**
```
User: "Explain how machine learning algorithms work"
Response: Deep dive into algorithm mechanics, mathematics, optimization, 
          different algorithm types, and practical applications
```

## 🎯 Supported Learning Domains

- **🐍 Python Development** - Django, Flask, FastAPI, data science
- **🌐 Web Development** - React, Vue, Angular, Node.js, JavaScript
- **🤖 AI Engineering** - Machine learning, deep learning, neural networks
- **⛓️ Web3 Development** - Blockchain, smart contracts, DApps, DeFi
- **🔒 Cybersecurity** - Ethical hacking, penetration testing, network security
- **☁️ DevOps** - Docker, Kubernetes, AWS, Azure, GCP
- **📱 Mobile Development** - iOS, Android, React Native, Flutter
- **🎨 UI/UX Design** - User interface, user experience, Figma, Adobe
- **🗄️ Database** - SQL, MongoDB, PostgreSQL, Redis
- **⚙️ Software Engineering** - Programming, algorithms, data structures
- **And many more!** - Dynamic domain detection for any educational topic

## 🔧 Advanced Features

### **MeTTa Knowledge Graph Integration**
- **Automatic Detection**: Uses real MeTTa when hyperon is installed
- **Graceful Fallback**: Works with mock data when hyperon unavailable
- **Structured Learning**: Concept relationships and learning dependencies
- **Prerequisite Mapping**: Optimal learning sequence recommendations

### **Smart Query Processing**
- **Intent Recognition**: Automatically detects user learning goals
- **Context Analysis**: Understands specific learning requirements
- **Domain Extraction**: Dynamically identifies relevant learning domains
- **Personalized Responses**: Tailored to individual learning needs

### **Inter-Agent Communication**
- **Request Tracking**: Unique request IDs for response coordination
- **Message Routing**: Intelligent routing based on query intent
- **Response Forwarding**: Seamless user experience across agents
- **Error Handling**: Robust error handling and fallback mechanisms

## 📁 Project Structure

```
eduFinder/
├── agents/                    # Specialized AI agents
│   ├── curriculum_agent.py   # Educational plan creation
│   ├── materials_agent.py   # Resource discovery
│   └── enhanced_agent.py    # Deep insights
├── services/                 # Core services
│   ├── gemini_service.py   # Gemini AI integration
│   └── metta_integration.py # MeTTa knowledge graph
├── config.py                # Configuration management
├── models.py                # Data models for inter-agent communication
├── agent.py                 # Main routing agent
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Development

### **Adding New Learning Domains**
The system automatically detects new domains from user queries. No hardcoding required!

### **Extending Agent Capabilities**
Each agent can be extended with new functionality while maintaining the same communication interface.

### **Customizing Responses**
Modify the Gemini prompts in `services/gemini_service.py` to customize response formats and content.

## 🙏 Acknowledgments

- **uAgents Framework** - Autonomous AI agent communication
- **Google Gemini AI** - Advanced content generation
- **MeTTa Language** - Knowledge graph and reasoning
- **YouTube API** - Educational video discovery

---

**EduFinder** - Empowering learners with intelligent, personalized educational experiences! 🎓✨