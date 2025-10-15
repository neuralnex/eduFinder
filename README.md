# 🎓 Learning Path Agents - ASI Alliance Hackathon

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## 🚀 Project Overview

**Learning Path Agents** is an autonomous AI system that creates personalized learning curricula and provides educational materials for learners. Built for the ASI Alliance Hackathon, this project demonstrates the power of decentralized AI agents working together to solve real-world educational challenges.

### 🎯 What We Built

Our system consists of three specialized AI agents that collaborate to provide comprehensive learning experiences:

1. **📚 Curriculum Agent** - Creates structured learning paths and curricula
2. **🎥 Materials Agent** - Sources educational videos and learning resources  
3. **🧠 Enhanced Learning Agent** - Integrates MeTTa Knowledge Graph for intelligent curriculum planning

## ✨ Key Features

- **🎯 Personalized Learning Paths**: AI agents create customized curricula based on learner needs
- **📚 Comprehensive Resource Discovery**: Automatically sources YouTube videos, courses, books, and projects
- **🧠 Knowledge Graph Integration**: Uses MeTTa to understand concept relationships and dependencies
- **🤖 Multi-Agent Collaboration**: Agents communicate and work together seamlessly
- **🌐 ASI:One Compatible**: Full Chat Protocol integration for human interaction
- **📱 Agentverse Registered**: Agents are discoverable and deployable on the ASI ecosystem

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Curriculum     │    │  Materials      │    │  Enhanced       │
│  Agent          │◄──►│  Agent          │◄──►│  Learning Agent │
│                 │    │                 │    │                 │
│ • Creates paths │    │ • Sources videos│    │ • MeTTa Graph   │
│ • Structures    │    │ • Finds courses │    │ • Deep insights │
│   curricula     │    │ • Recommends    │    │ • Smart paths   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   ASI:One Chat   │
                    │   Protocol       │
                    │                 │
                    │ • Human access  │
                    │ • Agent discovery│
                    │ • Conversation  │
                    └─────────────────┘
```

## Project Structure

```
eduFinder/
├── agents/                        # Agent implementations
│   ├── __init__.py
│   ├── curriculum_agent.py        # Curriculum creation specialist
│   ├── materials_agent.py         # Resource discovery specialist
│   └── enhanced_agent.py          # Deep insights specialist
├── services/                      # Service implementations
│   ├── __init__.py
│   ├── gemini_service.py          # Gemini AI integration service
│   └── metta_integration.py       # MeTTa knowledge graph integration
├── agent.py                       # Main unified agent interface
├── app.py                         # Multi-agent launcher
├── config.py                      # Configuration management
├── requirements.txt               # Dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
└── .gitattributes                 # Git attributes
```

## 🚀 Inter-Agent Communication System

The system uses modern uAgents message passing for seamless communication between specialized agents:

### **📋 Communication Flow:**
1. **User Query** → Main Agent (agent.py)
2. **Main Agent** → Routes to Specialized Agent
3. **Specialized Agent** → Processes with Gemini AI
4. **Specialized Agent** → Sends Response back to Main Agent
5. **Main Agent** → Delivers Response to User

### **🔧 Message Models:**
- `Request/Response` - General agent communication
- `CurriculumRequest/Response` - Curriculum-specific communication
- `MaterialsRequest/Response` - Materials-specific communication
- `InsightsRequest/Response` - Insights-specific communication

### **🎯 Agent Addresses:**
- **Main Agent**: `agent1q0zgf9tmxl5rt4aurgx4uv0qhzmur2hzqzzhatrnd59hymvs0y2jz5m68q8` (Port 8000)
- **Curriculum Agent**: `agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8` (Port 8001)
- **Materials Agent**: `agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf` (Port 8002)
- **Enhanced Agent**: `agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4` (Port 8003)

## 🛠️ Technology Stack

### Core Technologies
- **uAgents Framework**: Fetch.ai's agent framework for autonomous AI
- **Gemini AI**: Google's AI for content generation and insights
- **YouTube Search API**: Real-time educational video discovery
- **Chat Protocol**: ASI-wide communication standard
- **Agentverse**: ASI ecosystem registry and orchestration layer

### Supporting Technologies
- **Python 3.8+**: Core programming language
- **aiohttp**: Asynchronous HTTP client
- **Pydantic**: Data validation and serialization
- **Environment Variables**: Configuration management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/learning-path-agents.git
   cd learning-path-agents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the deployment script**
   ```bash
   python deploy.py
   ```

### Running the System

**Start All Agents**
```bash
python app.py
```

**Start Individual Agents**
```bash
# Curriculum Agent (port 8001)
python agents/curriculum_agent.py

# Materials Agent (port 8002)
python agents/materials_agent.py

# Enhanced Agent (port 8003)
python agents/enhanced_agent.py
```

The system provides three specialized agents:
- **Curriculum Agent** - Creates structured learning paths
- **Materials Agent** - Discovers educational resources  
- **Enhanced Agent** - Provides deep insights via MeTTa

## 🎯 Agent Details

### 📚 Curriculum Agent
- **Port**: 8001
- **Name**: CurriculumAgent
- **Description**: Specializes in creating structured learning paths and curricula
- **Capabilities**:
  - **Curriculum Creation** - Structured learning paths for various domains
  - **Learning Module Organization** - Break down complex subjects into manageable steps
  - **Prerequisite Identification** - Show what you need to learn first
  - **Learning Sequence Planning** - Optimal order for mastering concepts

### 🎥 Materials Agent
- **Port**: 8002
- **Name**: MaterialsAgent
- **Description**: Specializes in discovering and providing educational resources
- **Capabilities**:
  - **Resource Discovery** - Educational videos, courses, books, and projects
  - **YouTube Search** - Real-time educational content discovery
  - **Learning Materials** - Curated resources for specific topics
  - **Project Suggestions** - Hands-on exercises and practical applications

### 🧠 Enhanced Learning Agent
- **Port**: 8003
- **Name**: EnhancedAgent
- **Description**: Provides deep insights using MeTTa Knowledge Graph integration
- **Capabilities**:
  - **Knowledge Graph Integration** - Understands concept relationships and dependencies
  - **Deep Concept Analysis** - Explains how different topics connect
  - **Prerequisite Mapping** - Knows what you need to learn before advanced topics
  - **Learning Sequence Optimization** - Suggests the best order to learn concepts
  - **Cross-Domain Connections** - Shows how concepts relate across different fields

### 🧠 MeTTa Knowledge Graph Integration
- **Purpose**: Provides intelligent concept relationships and learning dependencies
- **Features**:
  - Concept prerequisite mapping
  - Learning path optimization
  - Cross-domain knowledge connections
  - Smart learning sequence suggestions

### 🔍 RAG (Retrieval-Augmented Generation) System
- **Purpose**: Provides comprehensive learning resources and intelligent responses
- **Features**:
  - Learning domain management (AI Engineering, Web3 Development, Data Science)
  - Educational resource curation (videos, courses, books, projects)
  - YouTube search integration for real-time content discovery
  - MeTTa knowledge graph integration for deep insights
  - Intelligent request routing and response generation

## 🔧 Configuration

### Environment Variables
```bash
# Agent Configuration
AGENT_SEED=your-main-agent-seed-here

# Individual Agent Seeds
CURRICULUM_AGENT_SEED=curriculum_agent_seed_2024
MATERIALS_AGENT_SEED=materials_agent_seed_2024
ENHANCED_AGENT_SEED=enhanced_agent_seed_2024

# AI Services
GEMINI_API_KEY=your-gemini-api-key-here
YOUTUBE_API_KEY=your-youtube-api-key

# MeTTa Knowledge Graph
METTA_ENDPOINT=http://localhost:8080
METTA_SPACE=learning_space
METTA_USE_MOCK=false

# Agentverse
AGENTVERSE_ENDPOINT=https://agentverse.ai
```

## 📖 Usage Examples

### Basic Curriculum Creation
```
User: "Teach me AI engineering"
Agent: Creates a comprehensive AI engineering curriculum with:
- Foundations of AI (4-6 weeks)
- Deep Learning Fundamentals (6-8 weeks)  
- AI Engineering Practices (8-10 weeks)
- Specialized Applications (6-8 weeks)
```

### Resource Discovery
```
User: "Get me resources for machine learning"
Agent: Provides:
- Recommended YouTube videos
- Online courses
- Books
- Hands-on projects
- Learning tips
```

### Knowledge Graph Integration
```
User: "Explain deep learning concepts"
Agent: Uses MeTTa to provide:
- Concept definitions
- Prerequisites
- Related concepts
- Learning dependencies
- Optimal learning path
```

## 🌐 ASI Alliance Integration

### Agentverse Registration
All agents are registered on Agentverse with:
- ✅ Chat Protocol enabled
- ✅ ASI:One compatibility
- ✅ Agent discovery
- ✅ Manifest publishing

### Chat Protocol Features
- **Start Session**: Welcome message and capabilities
- **Text Messages**: Natural language interaction
- **End Session**: Farewell and next steps
- **Acknowledgements**: Reliable message delivery

### MeTTa Knowledge Graph
- **Concept Queries**: Deep understanding of learning topics
- **Relationship Mapping**: How concepts connect and depend on each other
- **Learning Paths**: Optimal sequences for skill development
- **Prerequisite Analysis**: What you need to know before learning advanced topics

## 🎥 Demo Video

[Demo Video Link - Coming Soon]

The demo showcases:
- Agent interaction and communication
- Curriculum creation process
- Resource discovery and recommendation
- MeTTa Knowledge Graph integration
- ASI:One chat interface

## 🏆 Hackathon Criteria Alignment

### ✅ Functionality & Technical Implementation (25%)
- **Multi-agent system** with real-time communication
- **Working curriculum generation** with structured learning paths
- **Resource discovery** with YouTube integration
- **MeTTa Knowledge Graph** integration for intelligent planning

### ✅ Use of ASI Alliance Tech (20%)
- **uAgents Framework**: Core agent implementation
- **Agentverse Registration**: All agents registered and discoverable
- **Chat Protocol**: Full ASI:One compatibility
- **MeTTa Integration**: Knowledge graph for structured learning data

### ✅ Innovation & Creativity (20%)
- **Novel approach** to personalized education using AI agents
- **Multi-agent collaboration** for comprehensive learning support
- **Knowledge graph integration** for intelligent curriculum planning
- **Decentralized learning** ecosystem

### ✅ Real-World Impact & Usefulness (20%)
- **Solves real problem**: Personalized education at scale
- **Practical application**: Works for multiple learning domains
- **User-friendly**: Natural language interaction
- **Scalable solution**: Can be extended to any learning domain

### ✅ User Experience & Presentation (15%)
- **Clear documentation** with setup instructions
- **Intuitive interaction** through natural language
- **Comprehensive features** covering the entire learning journey
- **Professional presentation** with badges and structure

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on:
- Code style and standards
- Testing requirements
- Documentation updates
- Feature requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **ASI Alliance** for providing the platform and resources
- **Fetch.ai** for the uAgents framework
- **SingularityNET** for MeTTa Knowledge Graph technology
- **Hackathon organizers** for creating this amazing opportunity

## 📞 Contact

- **Project Lead**: [Omeziri Zion Echezona]
- **Email**: [Omezirizion@gmail.com]
- **GitHub**: [neuralnex]
- **Agent Addresses**: Available after deployment

---

**Built with ❤️ for the ASI Alliance Hackathon**

*Empowering learners through autonomous AI agents* 🎓✨