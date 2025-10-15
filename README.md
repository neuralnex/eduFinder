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

## 📁 Project Structure

```
eduFinder/
├── agents/                          # 🤖 AI Agents Package
│   ├── __init__.py                 # Package initialization
│   ├── curriculum_agent.py         # 📚 Curriculum planning agent
│   ├── materials_agent.py          # 🎥 Resource discovery agent  
│   ├── enhanced_curriculum_agent.py # 🧠 MeTTa-integrated agent
│   └── metta_integration.py        # 🔧 Knowledge graph integration
├── config.py                       # ⚙️ Configuration management
├── requirements.txt                # 📦 Dependencies
├── deploy.py                       # 🚀 Deployment script
├── test_agents.py                  # 🧪 Test suite
├── demo.py                        # 🎬 Demo script
├── env.example                    # ⚙️ Environment template
├── setup.sh                       # 🛠️ Quick setup script
└── README.md                      # 📖 Comprehensive documentation
```

## 🛠️ Technology Stack

### Core Technologies
- **uAgents Framework**: Fetch.ai's agent framework for autonomous AI
- **MeTTa Knowledge Graph**: SingularityNET's knowledge representation system
- **Chat Protocol**: ASI-wide communication standard
- **Agentverse**: ASI ecosystem registry and orchestration layer

### Supporting Technologies
- **Python 3.8+**: Core programming language
- **YouTube Search API**: Educational video discovery
- **aiohttp**: Asynchronous HTTP client for MeTTa integration
- **Pydantic**: Data validation and serialization

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

### Running Individual Agents

**Curriculum Agent**
```bash
python agents/curriculum_agent.py
```

**Materials Agent**
```bash
python agents/materials_agent.py
```

**Enhanced Learning Agent (with MeTTa)**
```bash
python agents/enhanced_curriculum_agent.py
```

## 🎯 Agent Details

### 📚 Curriculum Agent
- **Address**: `agent1q...` (generated on first run)
- **Purpose**: Creates structured learning paths for various domains
- **Capabilities**:
  - AI Engineering curriculum
  - Web3 Development path
  - Data Science learning plan
  - Personalized difficulty adjustment

### 🎥 Materials Agent  
- **Address**: `agent1q...` (generated on first run)
- **Purpose**: Sources educational videos and learning resources
- **Capabilities**:
  - YouTube video discovery
  - Course recommendations
  - Book suggestions
  - Project ideas
  - Learning tips and schedules

### 🧠 Enhanced Learning Agent
- **Address**: `agent1q...` (generated on first run)
- **Purpose**: Intelligent curriculum planning with knowledge graph
- **Capabilities**:
  - MeTTa Knowledge Graph integration
  - Concept relationship understanding
  - Prerequisite analysis
  - Optimal learning sequence suggestion
  - Deep concept explanations

## 🔧 Configuration

### Environment Variables
```bash
# Agent Configuration
AGENT_SEED=your-unique-seed-here
AGENT_NAME=LearningPathAgent

# Optional: YouTube API for enhanced search
YOUTUBE_API_KEY=your-youtube-api-key

# MeTTa Knowledge Graph
METTA_ENDPOINT=http://localhost:8080

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

- **Project Lead**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [yourusername]
- **Agent Addresses**: Available after deployment

---

**Built with ❤️ for the ASI Alliance Hackathon**

*Empowering learners through autonomous AI agents* 🎓✨