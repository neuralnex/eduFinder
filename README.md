![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# Use python version 3.12*

# 🚀 EduFinder - AI-Powered Learning Path System

**EduFinder** is an intelligent multi-agent system that creates personalized educational plans, discovers targeted learning resources, and provides deep insights for ANY domain. Built with **uAgents** framework and powered by **Gemini AI** and **MeTTa Knowledge Graph** for unlimited learning capabilities.

## 🧠 **MeTTa Knowledge Graph Integration**

**EduFinder leverages the power of MeTTa Knowledge Graph for intelligent learning:**

### **🔬 Dynamic Knowledge Management**
- **Real-time Concept Analysis**: MeTTa dynamically analyzes any learning concept
- **Prerequisite Mapping**: AI-powered dependency analysis using knowledge graph
- **Learning Path Optimization**: Intelligent sequencing based on concept relationships
- **Cross-Domain Connections**: Reveals how concepts relate across different fields
- **Adaptive Difficulty Assessment**: Dynamic difficulty scoring based on concept complexity

### **⚡ Advanced MeTTa Operations**
- **`analyze-concept`**: Dynamic concept analysis using AI
- **`detect-domain`**: Intelligent domain detection from any query
- **`find-relationships`**: Concept relationship mapping and dependency analysis
- **Dynamic Knowledge Expansion**: Real-time knowledge graph updates
- **Grounded Atoms**: External data integration and Python object embedding

### **🎯 Unlimited Domain Support**
The MeTTa integration enables support for ANY educational domain:
- **Technology**: Programming, AI, Web3, Data Science, DevOps, Cybersecurity
- **Creative Arts**: Design, Music, Art, Photography, Creative Writing
- **Sciences**: Physics, Chemistry, Biology, Mathematics, Research Methods
- **Languages**: English, Spanish, French, Linguistics, Grammar
- **Life Skills**: Cooking, Fitness, Psychology, Philosophy, History
- **Business**: Marketing, Finance, Management, Entrepreneurship
- **And ANYTHING else you want to learn!**

### **🔧 MeTTa Configuration**
```bash
# Install MeTTa (hyperon)
pip install hyperon

# Configure MeTTa settings
METTA_ENDPOINT=http://localhost:8080
METTA_SPACE=learning_space
METTA_USE_MOCK=false  # Set to true for demo mode
```

## ✨ Agent Powers & Capabilities

### 🚀 **Main Routing Agent** - The Intelligent Orchestrator
**Agent Address**: `agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne`

**🔥 Core Powers:**
- **🧠 Smart Query Analysis**: Uses Gemini AI + MeTTa Knowledge Graph to understand user intent and extract learning topics
- **🎯 Intelligent Routing**: Automatically routes requests to the most appropriate specialized agent
- **🔄 Request Orchestration**: Manages complex multi-agent workflows with unique request tracking
- **💬 Natural Greeting Handling**: Responds naturally to greetings and provides comprehensive system overview
- **🌐 Universal Domain Support**: Handles ANY educational domain dynamically using MeTTa knowledge graph
- **⚡ Real-time Coordination**: Seamlessly coordinates responses from multiple agents back to users

**🎯 Routing Intelligence:**
- **Curriculum Requests**: Detects "teach me", "learn", "curriculum", "learning path" → Routes to Curriculum Agent
- **Resource Requests**: Detects "resources", "find", "videos", "courses" → Routes to Materials Agent  
- **Insight Requests**: Detects "explain", "understand", "insights", "analysis" → Routes to Enhanced Agent

---

### 📚 **Curriculum Agent** - The Learning Path Architect
**Agent Address**: `agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8`

**🔥 Core Powers:**
- **🏗️ Dynamic Learning Architecture**: Creates comprehensive, step-by-step learning paths for ANY domain using MeTTa knowledge graph
- **🎯 AI-Powered Prerequisite Intelligence**: Automatically identifies what learners need to know first using MeTTa concept analysis
- **📈 Adaptive Difficulty Progression**: Designs optimal progression from beginner to advanced levels using MeTTa difficulty assessment
- **⏱️ Intelligent Time Management**: Provides realistic time estimates using MeTTa learning path analysis
- **🎨 Personalized Curricula**: Tailors learning paths to specific user goals using dynamic MeTTa insights
- **🔗 Dynamic Concept Integration**: Shows how different topics connect using MeTTa relationship mapping

**🎯 Specialized Capabilities:**
- **Unlimited Domain Support**: Handles ANY educational domain using MeTTa knowledge graph
- **Dynamic Learning Module Organization**: Breaks complex subjects into manageable steps using MeTTa analysis
- **AI-Powered Learning Sequence Optimization**: Determines optimal order using MeTTa concept relationships
- **Intelligent Practice Integration**: Includes hands-on exercises using MeTTa learning path insights

---

### 🎥 **Materials Agent** - The Resource Discovery Specialist
**Agent Address**: `agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf`

**🔥 Core Powers:**
- **🔍 Dynamic Resource Discovery**: Finds the most relevant educational materials instantly using MeTTa knowledge graph insights
- **🎥 Intelligent YouTube Integration**: Discovers educational videos with detailed metadata using AI-powered analysis
- **📚 Multi-format Resource Curation**: Curates courses, books, documentation, tutorials using MeTTa concept analysis
- **🔗 Direct Link Provision**: Provides clickable links to all discovered resources
- **⭐ AI-Powered Quality Filtering**: Uses MeTTa + Gemini AI to assess and recommend high-quality learning materials
- **🌐 Universal Resource Access**: Searches across multiple platforms for ANY educational domain

**🎯 Specialized Capabilities:**
- **Video Metadata Extraction**: Provides detailed information about YouTube videos (channel, duration, views, published date)
- **Resource Categorization**: Organizes materials by type (courses, tutorials, documentation, practice platforms)
- **Learning Style Adaptation**: Finds resources that match different learning preferences
- **Recent Content Discovery**: Prioritizes up-to-date and current educational materials

---

### 🧠 **Enhanced Agent** - The Deep Insights Analyst
**Agent Address**: `agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4`

**🔥 Core Powers:**
- **🔬 Dynamic Concept Analysis**: Provides comprehensive explanations using MeTTa knowledge graph + Gemini AI
- **🗺️ AI-Powered Prerequisite Mapping**: Creates detailed maps using MeTTa concept relationships and dependencies
- **🔗 Cross-Domain Connection Analysis**: Reveals how concepts relate across different fields using MeTTa insights
- **📊 Intelligent Learning Dependency Analysis**: Shows optimal learning sequences using MeTTa knowledge graph
- **🎯 Advanced AI Insights**: Uses MeTTa + Gemini AI fusion for nuanced understanding and analysis
- **🧩 Dynamic Conceptual Framework Building**: Helps learners build mental models using MeTTa concept relationships

**🎯 Specialized Capabilities:**
- **Concept Relationship Mapping**: Explains how different topics connect and build upon each other
- **Learning Sequence Optimization**: Recommends the best order to learn concepts for maximum understanding
- **Metacognitive Analysis**: Helps learners understand how to learn more effectively
- **Strategic Learning Guidance**: Provides insights into learning strategies and approaches

## 🏗️ System Architecture

### **Multi-Agent Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                🚀 Main Routing Agent                        │
│              The Intelligent Orchestrator                   │
│                     (Port 8000)                            │
│  🧠 Smart Query Analysis & Intent Recognition              │
│  🎯 Intelligent Routing & Request Orchestration           │
│  🔄 Multi-Agent Coordination & Response Management        │
│  💬 Natural Greeting Handling & System Overview            │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 📚 Curriculum│ │ 🎥 Materials│ │ 🧠 Enhanced │
│    Agent     │ │    Agent    │ │    Agent    │
│ (Port 8001)  │ │ (Port 8002) │ │ (Port 8003) │
│              │ │             │ │             │
│ 🏗️ Learning  │ │ 🔍 Resource │ │ 🔬 Deep     │
│   Path       │ │   Discovery │ │   Insights  │
│   Architect  │ │   Specialist│ │   Analyst   │
│              │ │             │ │             │
│ • Structured │ │ • Real-time │ │ • Concept   │
│   Learning   │ │   Resource  │ │   Analysis  │
│   Paths      │ │   Discovery │ │ • Prereq    │
│ • Prereq     │ │ • YouTube   │ │   Mapping   │
│   Intelligence│ │   Integration│ │ • Cross-    │
│ • Difficulty │ │ • Multi-    │ │   Domain    │
│   Progression│ │   format    │ │   Connections│
│ • Time       │ │   Resources │ │ • Learning  │
│   Management │ │ • Quality   │ │   Dependencies│
│              │ │   Filtering │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
```

## ⚡ Agent Synergy & Power Combinations

### 🔥 **Dynamic Learning Ecosystem**
The agents work together to create a comprehensive learning experience:

**🎯 Complete Learning Journey:**
1. **Main Agent** → Analyzes user intent and routes to appropriate specialist
2. **Curriculum Agent** → Creates structured learning path with prerequisites
3. **Materials Agent** → Discovers relevant resources and videos for each step
4. **Enhanced Agent** → Provides deep insights and concept relationships

**🚀 Power Combinations:**
- **📚 + 🎥**: Curriculum Agent creates learning path → Materials Agent finds resources for each step
- **🧠 + 📚**: Enhanced Agent explains concepts → Curriculum Agent structures learning sequence
- **🎥 + 🧠**: Materials Agent finds resources → Enhanced Agent explains how concepts connect
- **🚀 + All**: Main Agent orchestrates multi-agent workflows for complex learning requests

**💡 Intelligent Workflows:**
- **"Teach me React"** → Main Agent routes to Curriculum Agent → Creates comprehensive React learning path
- **"Find Python resources"** → Main Agent routes to Materials Agent → Discovers videos, courses, documentation
- **"Explain machine learning"** → Main Agent routes to Enhanced Agent → Provides deep conceptual analysis
- **"Create a cybersecurity curriculum with resources"** → Main Agent coordinates Curriculum + Materials Agents

### **Technology Stack**
- **🤖 uAgents Framework**: Autonomous AI agent communication
- **🧠 Gemini AI**: Google's AI for content generation and analysis
- **📊 MeTTa Knowledge Graph (Hyperon)**: Advanced knowledge representation and reasoning
- **⚡ Dynamic MeTTa Operations**: Real-time concept analysis, domain detection, and relationship mapping
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

pip install hyperon

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

### **Testing MeTTa Integration**
```bash
# Test MeTTa integration
python test_metta_integration.py

# Install hyperon for real MeTTa (optional)
pip install hyperon

# Set environment variable to use real MeTTa
export METTA_USE_MOCK=false
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

## 🎯 **Unlimited Learning Domains**

**EduFinder supports ANY educational domain using MeTTa knowledge graph:**

### **Technology Domains**
- **🐍 Python Development** - Django, Flask, FastAPI, data science
- **🌐 Web Development** - React, Vue, Angular, Node.js, JavaScript
- **🤖 AI Engineering** - Machine learning, deep learning, neural networks
- **⛓️ Web3 Development** - Blockchain, smart contracts, DApps, DeFi
- **🔒 Cybersecurity** - Ethical hacking, penetration testing, network security
- **☁️ DevOps** - Docker, Kubernetes, AWS, Azure, GCP
- **📱 Mobile Development** - iOS, Android, React Native, Flutter

### **Creative & Arts Domains**
- **🎨 UI/UX Design** - User interface, user experience, Figma, Adobe
- **🎵 Music** - Guitar, piano, singing, composition, audio production
- **🎭 Art** - Drawing, painting, sculpture, digital art, photography
- **✍️ Creative Writing** - Poetry, novels, storytelling, screenwriting

### **Academic Domains**
- **🔬 Sciences** - Physics, chemistry, biology, mathematics, research methods
- **📚 Languages** - English, Spanish, French, linguistics, grammar
- **🧠 Psychology** - Mental health, therapy, counseling, behavior analysis
- **🤔 Philosophy** - Ethics, logic, metaphysics, critical thinking
- **📖 Literature** - Writing, poetry, novel analysis, creative writing

### **Life Skills Domains**
- **🍳 Cooking** - Culinary arts, baking, recipe development, food science
- **💪 Fitness** - Exercise, workout routines, yoga, running, training
- **📈 Business** - Marketing, finance, management, entrepreneurship
- **📚 History** - World history, ancient civilizations, modern events

### **🚀 Dynamic Domain Detection**
**No hardcoded limitations!** EduFinder uses MeTTa knowledge graph to dynamically detect and support ANY educational topic you want to learn.

## 🔧 Advanced Features

### **🧠 MeTTa Knowledge Graph Integration**
- **Dynamic Knowledge Management**: Real-time concept analysis and knowledge graph expansion
- **Advanced MeTTa Operations**: `analyze-concept`, `detect-domain`, `find-relationships` operations
- **Intelligent Fallback**: Pure Gemini AI when hyperon is not installed
- **Enhanced Curriculum Generation**: Prerequisites and learning paths from MeTTa knowledge graph
- **Deep Insights Integration**: Concept relationships and dependencies from MeTTa
- **Smart Detection**: Automatically detects hyperon availability and adjusts behavior
- **Unlimited Domain Support**: Dynamic domain detection for ANY educational topic

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
├── test_metta_integration.py # MeTTa integration test script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔗 AgentVerse Inspection Links

### **Agent Profile URLs**
Access each agent's profile directly through AgentVerse:

- **Main Agent**: https://agentverse.ai/agents/details/agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne/profile
- **Curriculum Agent**: https://agentverse.ai/agents/details/agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8/profile
- **Materials Agent**: https://agentverse.ai/agents/details/agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf/profile
- **Enhanced Agent**: https://agentverse.ai/agents/details/agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4/profile

### **Agent Addresses**
- **Main Agent**: `agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne`
- **Curriculum Agent**: `agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8`
- **Materials Agent**: `agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf`
- **Enhanced Agent**: `agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4`

## 🛠️ Development

### **Adding New Learning Domains**
The system automatically detects new domains from user queries. No hardcoding required!

### **Extending Agent Capabilities**
Each agent can be extended with new functionality while maintaining the same communication interface.

### **Customizing Responses**
Modify the Gemini prompts in `services/gemini_service.py` to customize response formats and content.

## 🙏 Acknowledgments

- **uAgents Framework** - Autonomous AI agent communication
- **Google Gemini AI** - Advanced content generation and natural language understanding
- **MeTTa Language (Hyperon)** - Advanced knowledge representation, reasoning, and dynamic concept analysis
- **YouTube API** - Educational video discovery and metadata extraction

---

**EduFinder** - Empowering learners with intelligent, unlimited educational experiences powered by MeTTa Knowledge Graph and Gemini AI! 🎓✨