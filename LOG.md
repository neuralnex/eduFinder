# EduFinder Development Log

## Project Overview
EduFinder is a multi-agent learning path system built for the ASI Alliance Hackathon. It creates personalized learning curricula, discovers educational resources, and provides deep insights through AI-powered agents.

## Architecture Evolution

### Phase 1: MeTTa Integration Foundation
**Initial Setup**: Started with MeTTa knowledge graph integration using `hyperon` library.

**Key Components**:
- `metta_integration.py`: Core MeTTa query interface
- `METTA_SETUP.md`: Installation documentation
- `config.py`: Configuration management
- `env.example`: Environment variables template

**MeTTa Query Methods**:
```python
# Definition queries
definition_query = f'!(match &self (definition {concept_key} $def) $def)'

# Prerequisites queries  
prerequisites_query = f'!(match &self (prerequisites {concept_key} $prereq) $prereq)'

# Related concepts queries
related_query = f'!(match &self (related {concept_key} $related) $related)'

# Learning path queries
path_query = f'!(match &self (learning_path {concept_key} $path) $path)'

# Difficulty and time estimates
difficulty_query = f'!(match &self (difficulty {concept_key} $diff) $diff)'
time_query = f'!(match &self (time_estimate {concept_key} $time) $time)'
```

**Configuration Changes**:
- Modified `METTA_USE_MOCK` default from "true" to "false"
- Prioritized real MeTTa data over mock data
- Added proper error handling for MeTTa queries

### Phase 2: Agent Architecture Development

**Initial Agent Structure**:
- Individual agent files in `agents/` folder
- Each agent specialized for specific functionality
- Used `uAgents` framework for agent communication

**Agent Specializations**:
1. **Curriculum Agent**: Creates structured learning paths
2. **Materials Agent**: Discovers educational resources
3. **Enhanced Agent**: Provides deep insights and analysis

**Key Features**:
- Mailbox communication for ASI:One integration
- Custom message models for inter-agent communication
- Gemini AI integration for content generation
- YouTube API integration for video discovery

### Phase 3: Unified Agent System

**Architecture Decision**: Consolidated all agents into a single `agent.py` file for simplified deployment.

**Components**:
- Single `LearningPathAgent` with multiple capabilities
- Integrated curriculum, materials, and insights functionality
- Streamlined user interface

**Challenges**:
- Model registration conflicts with multiple agents
- Port management issues
- Import path complications

### Phase 4: Multi-Agent Coordination

**Final Architecture**: Split back into specialized agents with a main coordinator.

**Current Structure**:
```
agent.py (Main Router - Port 8000)
├── agents/curriculum_agent.py (Port 8001)
├── agents/materials_agent.py (Port 8002)
├── agents/enhanced_agent.py (Port 8003)
└── services/gemini_service.py
```

## Technical Implementation

### Agent Communication Protocol

**Message Models**:
```python
# Request Models
class CurriculumRequest(Model):
    domain: str
    user_query: str

class MaterialsRequest(Model):
    topic: str
    domain: str
    include_youtube: bool

class InsightsRequest(Model):
    concept: str
    domain: str
    query_type: str

# Response Models
class CurriculumResponse(Model):
    curriculum: str
    success: bool
    error: Optional[str] = None

class MaterialsResponse(Model):
    materials: str
    youtube_videos: str
    success: bool
    error: Optional[str] = None

class InsightsResponse(Model):
    insights: str
    success: bool
    error: Optional[str] = None
```

**Inter-Agent Communication Flow**:
1. User sends message to main agent (port 8000)
2. Main agent analyzes message content
3. Routes request to appropriate specialized agent
4. Specialized agent processes request using Gemini AI
5. Response sent back to main agent
6. Main agent delivers response to user

### Gemini AI Integration

**Service Implementation**:
```python
class GeminiLearningService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
    
    async def generate_curriculum(self, domain: str) -> str:
        # Generates structured learning paths
    
    async def generate_learning_materials(self, topic: str, domain: str) -> str:
        # Creates educational resource lists
    
    async def generate_deep_insights(self, concept: str, domain: str) -> str:
        # Provides concept analysis and relationships
    
    async def search_youtube_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        # Searches for relevant educational videos
```

### Agent Configuration

**Environment Variables**:
```python
# Agent Seeds
AGENT_SEED = "main_learning_agent_seed_2024"
CURRICULUM_AGENT_SEED = "curriculum_agent_seed_2024"
MATERIALS_AGENT_SEED = "materials_agent_seed_2024"
ENHANCED_AGENT_SEED = "enhanced_agent_seed_2024"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# MeTTa Configuration
METTA_USE_MOCK = os.getenv("METTA_USE_MOCK", "false")
```

**Agent Initialization**:
```python
# Main Router Agent
learning_agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=8000,
    mailbox=True
)

# Specialized Agents
curriculum_agent = Agent(
    name="CurriculumAgent",
    seed=CURRICULUM_AGENT_SEED,
    port=8001,
    mailbox=True
)
```

## Key Features

### 1. Curriculum Creation
- **Domain Support**: AI Engineering, Web3 Development, Data Science
- **Structured Learning Paths**: Step-by-step progression
- **Prerequisite Mapping**: Identifies required prior knowledge
- **Difficulty Progression**: Beginner to advanced levels

### 2. Resource Discovery
- **Educational Materials**: Courses, books, tutorials
- **YouTube Integration**: Real-time video search
- **Project Suggestions**: Hands-on learning opportunities
- **Resource Curation**: Quality-filtered content

### 3. Deep Insights
- **Concept Relationships**: How topics connect
- **Learning Dependencies**: Prerequisite identification
- **Cross-Domain Connections**: Interdisciplinary learning
- **Knowledge Graph Integration**: MeTTa-powered analysis

### 4. Inter-Agent Communication
- **Intelligent Routing**: Message analysis and delegation
- **Response Aggregation**: Combined insights from multiple agents
- **Fault Tolerance**: Error handling and fallback mechanisms
- **Scalable Architecture**: Easy addition of new specialized agents

## Deployment Architecture

### Agent Addresses
- **Main Router**: `agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne`
- **Curriculum Agent**: `agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8`
- **Materials Agent**: `agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf`
- **Enhanced Agent**: `agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4`

### Port Configuration
- **Main Agent**: Port 8000
- **Curriculum Agent**: Port 8001
- **Materials Agent**: Port 8002
- **Enhanced Agent**: Port 8003

### Process Management
```bash
# Start individual agents
python3 agents/curriculum_agent.py
python3 agents/materials_agent.py
python3 agents/enhanced_agent.py

# Start main coordinator
python3 agent.py
```

## User Interaction Patterns

### 1. Direct Agent Access
Users can connect directly to specialized agents for specific functionality:
- **Curriculum Agent**: "Teach me AI engineering"
- **Materials Agent**: "Find machine learning resources"
- **Enhanced Agent**: "Explain deep learning concepts"

### 2. Coordinated Access
Users connect to main agent for comprehensive learning support:
- **Intelligent Routing**: Automatically delegates to appropriate agents
- **Combined Responses**: Aggregates insights from multiple agents
- **Unified Interface**: Single point of interaction

### 3. Message Processing
```python
# Curriculum requests
if any(keyword in user_input for keyword in ["curriculum", "teach me", "learning path"]):
    await ctx.send(CURRICULUM_AGENT_ADDRESS, CurriculumRequest(...))

# Materials requests  
elif any(keyword in user_input for keyword in ["resources", "find", "videos"]):
    await ctx.send(MATERIALS_AGENT_ADDRESS, MaterialsRequest(...))

# Insights requests
elif any(keyword in user_input for keyword in ["explain", "how does", "concept"]):
    await ctx.send(ENHANCED_AGENT_ADDRESS, InsightsRequest(...))
```

## Technology Stack

### Core Technologies
- **uAgents Framework**: Agent communication and management
- **Gemini AI**: Content generation and analysis
- **MeTTa/Hyperon**: Knowledge graph integration
- **YouTube API**: Video discovery and metadata
- **Python 3.8+**: Primary development language

### Dependencies
```
uagents>=0.7.0
google-genai>=0.3.0
hyperon>=0.2.8
youtubesearchpython>=1.6.0
python-dotenv>=1.0.0
```

### External Services
- **ASI:One**: Agent marketplace and communication
- **Google Gemini**: AI content generation
- **YouTube Data API**: Video search and metadata
- **MeTTa Knowledge Graph**: Concept relationships

## Development Challenges & Solutions

### 1. Port Management
**Problem**: Agents conflicting on same ports
**Solution**: Implemented unique port assignment (8000-8003) and process management

### 2. Model Registration Conflicts
**Problem**: Multiple agents using same protocol instances
**Solution**: Created unique Protocol instances for each agent

### 3. Import Path Issues
**Problem**: ModuleNotFoundError when running agents directly
**Solution**: Added proper sys.path configuration for subfolder imports

### 4. Mailbox Communication
**Problem**: Agents not responding in ASI:One interface
**Solution**: Removed conflicting endpoint configurations, ensured mailbox=True

### 5. Inter-Agent Communication
**Problem**: Complex message passing between agents
**Solution**: Implemented custom message models and response handlers

## Testing & Validation

### Agent Functionality Tests
- ✅ Curriculum generation for all domains
- ✅ Materials discovery with YouTube integration
- ✅ Deep insights and concept analysis
- ✅ Inter-agent message routing
- ✅ Error handling and fallback mechanisms

### Integration Tests
- ✅ ASI:One mailbox communication
- ✅ Gemini AI service integration
- ✅ YouTube API functionality
- ✅ MeTTa knowledge graph queries
- ✅ Multi-agent coordination

### Deployment Validation
- ✅ Individual agent startup
- ✅ Main coordinator functionality
- ✅ Port management and process control
- ✅ Environment variable configuration
- ✅ Logging and monitoring

## Future Enhancements

### Planned Features
1. **Advanced MeTTa Integration**: More sophisticated knowledge graph queries
2. **Learning Progress Tracking**: User progress monitoring
3. **Personalized Recommendations**: AI-driven learning suggestions
4. **Community Features**: User interaction and collaboration
5. **Mobile Interface**: Mobile app development

### Scalability Considerations
1. **Horizontal Scaling**: Multiple instances of specialized agents
2. **Load Balancing**: Intelligent request distribution
3. **Caching**: Response caching for improved performance
4. **Database Integration**: Persistent learning data storage

## Phase 6: Smart Query Understanding & Final Optimization (Latest)

### **Smart Query Understanding Implementation**
- **Enhanced Gemini Integration**: Updated all Gemini service methods to analyze specific user queries
- **Context-Aware Responses**: System now understands user intent and generates personalized content
- **Dynamic Query Processing**: Replaced hardcoded responses with intelligent query analysis

### **Key Improvements**
1. **Personalized Educational Plans**: Curriculum generation now tailored to specific user requests
2. **Targeted Resource Discovery**: Materials agent provides resources based on exact user needs
3. **Contextual Deep Insights**: Enhanced agent analyzes specific questions for relevant explanations

### **Technical Enhancements**
- **Query Parameter Passing**: All agents now receive and process user queries
- **Smart Prompt Engineering**: Gemini prompts updated to analyze user intent
- **Enhanced Response Quality**: More relevant and personalized learning content

### **System Architecture Final State**
```
Main Agent (Port 8000)
├── Curriculum Agent (Port 8001) - Smart educational plans
├── Materials Agent (Port 8002) - Targeted resource discovery  
└── Enhanced Agent (Port 8003) - Contextual deep insights
```

### **MeTTa Integration Status**
- **Smart Fallback System**: Automatically uses real MeTTa when hyperon installed
- **Graceful Degradation**: Falls back to mock data when hyperon unavailable
- **Windows Ready**: Prepared for testing with hyperon installation

## Conclusion

EduFinder represents a successful implementation of an intelligent multi-agent learning system that combines:
- **Smart Query Understanding** with context-aware AI responses
- **Specialized AI Agents** for different learning functions
- **Intelligent Coordination** through a main router agent
- **External AI Services** for personalized content generation
- **Knowledge Graph Integration** for deep insights
- **Scalable Architecture** for future enhancements

The system successfully demonstrates how multiple AI agents can work together to provide comprehensive, personalized educational support while maintaining individual specialization and coordinated communication.

### **Final Features**
✅ **Smart Query Analysis** - Understands user intent and context
✅ **Personalized Learning Plans** - Tailored to specific learning goals
✅ **Targeted Resource Discovery** - Finds relevant materials based on queries
✅ **Contextual Deep Insights** - Provides relevant concept explanations
✅ **MeTTa Knowledge Graph** - Structured learning concept relationships
✅ **Multi-Agent Coordination** - Seamless inter-agent communication
✅ **Production Ready** - Robust error handling and fallback systems

---

*Last Updated: December 2024*
*Version: 2.0.0*
*Status: Production Ready with Smart Query Understanding*
