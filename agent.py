
import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import uuid4

from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION, CURRICULUM_AGENT_SEED, MATERIALS_AGENT_SEED, ENHANCED_AGENT_SEED
from services.gemini_service import GeminiLearningService
from models import Request, Response, CurriculumRequest, MaterialsRequest, InsightsRequest, CurriculumResponse, MaterialsResponse, InsightsResponse

learning_agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=8000,
    mailbox=True
)

learning_chat_proto = Protocol(spec=chat_protocol_spec)

gemini_service = GeminiLearningService()

CURRICULUM_AGENT_ADDRESS = "agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8"
MATERIALS_AGENT_ADDRESS = "agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf"
ENHANCED_AGENT_ADDRESS = "agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4"

pending_requests = {}

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent())
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content
    )

def _extract_topic_from_query(query: str) -> str:
    query_lower = query.lower()
    
    common_tech_topics = [
        "python development", "python programming", "python", "django", "flask", "fastapi",
        "machine learning", "deep learning", "neural networks", "artificial intelligence",
        "blockchain", "smart contracts", "solidity", "ethereum", "web3",
        "data science", "data analysis", "statistics", "pandas", "numpy",
        "javascript", "typescript", "react", "nodejs", "vue", "angular",
        "java", "c++", "c#", "go", "rust", "swift", "kotlin",
        "frontend", "backend", "full stack", "mobile development", "ios", "android",
        "devops", "docker", "kubernetes", "aws", "azure", "gcp",
        "cybersecurity", "ethical hacking", "penetration testing",
        "game development", "unity", "unreal engine",
        "ui/ux design", "figma", "adobe", "design systems",
        "database", "sql", "mongodb", "postgresql", "redis",
        "microservices", "api development", "rest", "graphql",
        "cloud computing", "serverless", "lambda", "terraform",
        "machine learning ops", "mlops", "data engineering",
        "quantum computing", "robotics", "iot", "embedded systems"
    ]
    
    for topic in common_tech_topics:
        if topic in query_lower:
            return topic.replace(" ", "_")
    
    words = query_lower.split()
    if len(words) >= 2:
        return "_".join(words[:2])
    else:
        return words[0] if words else "general_learning"

def _extract_domain_from_query(query: str) -> str:
    query_lower = query.lower()
    
    domain_mappings = {
        "python_development": ["python development", "python programming", "python", "django", "flask", "fastapi", "python web", "python backend"],
        "ai_engineering": ["ai", "artificial intelligence", "machine learning", "deep learning", "neural networks", "ml", "dl"],
        "web3_development": ["web3", "blockchain", "smart contracts", "solidity", "ethereum", "crypto", "defi", "nft"],
        "data_science": ["data science", "data analysis", "statistics", "pandas", "numpy", "analytics", "big data"],
        "web_development": ["web development", "frontend", "backend", "full stack", "react", "vue", "angular", "nodejs", "javascript"],
        "mobile_development": ["mobile development", "ios", "android", "swift", "kotlin", "react native", "flutter"],
        "devops": ["devops", "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "infrastructure"],
        "cybersecurity": ["cybersecurity", "security", "ethical hacking", "penetration testing", "network security"],
        "game_development": ["game development", "unity", "unreal engine", "gaming", "game design"],
        "ui_ux_design": ["ui", "ux", "design", "figma", "adobe", "user interface", "user experience"],
        "cloud_computing": ["cloud", "aws", "azure", "gcp", "serverless", "lambda", "terraform"],
        "database": ["database", "sql", "mongodb", "postgresql", "redis", "data storage"],
        "software_engineering": ["software engineering", "programming", "coding", "algorithms", "data structures"]
    }
    
    for domain, keywords in domain_mappings.items():
        for keyword in keywords:
            if keyword in query_lower:
                return domain
    
    if any(word in query_lower for word in ["programming", "coding", "development", "software"]):
        return "software_engineering"
    elif any(word in query_lower for word in ["web", "html", "css", "javascript", "react", "vue"]):
        return "web_development"
    elif any(word in query_lower for word in ["mobile", "app", "ios", "android"]):
        return "mobile_development"
    else:
        return "general_tech"

@learning_chat_proto.on_message(ChatMessage)
async def handle_learning_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), 
        acknowledged_msg_id=msg.msg_id
    ))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_message = create_text_chat("""
**Welcome to EduFinder - Your AI Learning Companion!**

I'm your comprehensive learning assistant that creates personalized curricula, discovers educational resources, and provides deep insights for any technical domain.

**What I can help you with:**
• **Curriculum Creation** - Structured learning paths for any tech domain
• **Resource Discovery** - Educational videos, courses, books, and projects with links
• **Deep Insights** - Concept relationships and learning dependencies via Gemini AI
• **Personalized Learning** - Adapts to your skill level and goals

**Supported Learning Domains:**
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps, DeFi
• **Data Science** - Data analysis, statistics, machine learning
• **Web Development** - Frontend, backend, full-stack, React, Vue, Angular
• **Mobile Development** - iOS, Android, React Native, Flutter
• **DevOps** - Docker, Kubernetes, AWS, Azure, GCP
• **Cybersecurity** - Ethical hacking, penetration testing, network security
• **Game Development** - Unity, Unreal Engine, game design
• **UI/UX Design** - User interface, user experience, Figma, Adobe
• **Cloud Computing** - Serverless, Lambda, Terraform, infrastructure
• **Database** - SQL, MongoDB, PostgreSQL, Redis
• **Software Engineering** - Programming, algorithms, data structures
• **And many more!** - I can handle any educational or technical domain

**Try asking me:**
- "Teach me React development" (curriculum creation)
- "Find Python resources" (resource discovery)
- "Explain machine learning concepts" (deep insights)
- "Create a personalized learning path for cybersecurity"

What would you like to learn today?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            user_input = item.text.lower()
            
            if any(keyword in user_input for keyword in ["teach me", "learn", "educational plan", "learning plan", "study plan", "curriculum", "learning path", "create a", "help me learn"]):
                topic = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                
                import time
                request_id = f"educational_plan_{int(time.time())}_{topic}_{domain}"
                pending_requests[request_id] = sender
                
                await ctx.send(CURRICULUM_AGENT_ADDRESS, CurriculumRequest(
                    domain=domain,
                    user_query=item.text,
                    original_sender=sender,
                    request_id=request_id
                ))
                response = f"📚 Creating your comprehensive educational plan for {topic.replace('_', ' ').title()}..."
                
            elif any(keyword in user_input for keyword in ["resources", "find", "get me", "show me", "videos", "courses", "books", "tutorials", "materials"]):
                topic = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                
                import time
                request_id = f"materials_{int(time.time())}_{topic}_{domain}"
                pending_requests[request_id] = sender
                
                await ctx.send(MATERIALS_AGENT_ADDRESS, MaterialsRequest(
                    topic=topic,
                    domain=domain,
                    user_query=item.text,
                    include_youtube="youtube" in user_input or "videos" in user_input,
                    original_sender=sender,
                    request_id=request_id
                ))
                response = f"🎥 Finding targeted resources for {topic.replace('_', ' ').title()}..."
                
            elif any(keyword in user_input for keyword in ["explain", "how does", "what is", "concept", "relationship", "prerequisite", "deep insights"]):
                concept = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                
                import time
                request_id = f"insights_{int(time.time())}_{concept}_{domain}"
                pending_requests[request_id] = sender
                
                await ctx.send(ENHANCED_AGENT_ADDRESS, InsightsRequest(
                    concept=concept,
                    domain=domain,
                    query_type="explain",
                    user_query=item.text,
                    original_sender=sender,
                    request_id=request_id
                ))
                response = f"🧠 Generating deep insights about {concept.replace('_', ' ').title()}..."
                
            elif "help" in user_input or "what can you do" in user_input:
                response = """
**I'm your comprehensive Learning Path Agent!**

**My Capabilities:**

**📚 Educational Plan Creation** - I create complete learning paths with step-by-step resources
**🎥 Resource Discovery** - I find targeted learning materials, courses, and videos
**🧠 Deep Insights** - I explain concepts, relationships, and learning dependencies
**🎯 Personalized Learning** - I adapt plans to your skill level and goals

**What I Do:**
• **Comprehensive Plans**: Each step includes learning resources, links, and YouTube videos
• **Targeted Resources**: Find specific courses, tutorials, and materials based on your query
• **Structured Learning**: Clear progression from beginner to advanced
• **Resource Integration**: Direct links to courses, documentation, and tutorials
• **Deep Understanding**: Concept relationships and prerequisites

**Supported Domains:**
• **Python Development** - Django, Flask, FastAPI, data science
• **Web Development** - React, Vue, Angular, Node.js, JavaScript
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps, DeFi
• **Cybersecurity** - Ethical hacking, penetration testing, network security
• **DevOps** - Docker, Kubernetes, AWS, Azure, GCP
• **Mobile Development** - iOS, Android, React Native, Flutter
• **And many more!** - I can create plans for any educational domain

**Try asking me:**
- "Teach me Python development" (comprehensive educational plan)
- "Find React tutorials" (targeted resource discovery)
- "Explain machine learning concepts" (deep insights)
- "Help me learn cybersecurity" (personalized plan)

What would you like to learn?
                """
            else:
                if any(keyword in user_input for keyword in ["ai", "machine learning", "deep learning", "neural network"]):
                    response = f"""
I understand you want to learn about: "{item.text}"

Let me help you with AI Engineering! I can:

1. **Create a structured curriculum** - Tell me "teach me AI engineering"
2. **Find learning resources** - Ask me "find machine learning resources"  
3. **Explain concepts deeply** - Say "explain deep learning concepts"

**Available Learning Areas:**
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

What would you like me to help you with?
                    """
                elif any(keyword in user_input for keyword in ["blockchain", "web3", "smart contract", "cryptocurrency"]):
                    response = f"""
I understand you want to learn about: "{item.text}"

Let me help you with Web3 Development! I can:

1. **Create a structured curriculum** - Tell me "teach me blockchain development"
2. **Find learning resources** - Ask me "find blockchain resources"
3. **Explain concepts deeply** - Say "explain smart contracts"

**Available Learning Areas:**
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

What would you like me to help you with?
                    """
                elif any(keyword in user_input for keyword in ["data", "statistics", "analysis", "python"]):
                    response = f"""
I understand you want to learn about: "{item.text}"

Let me help you with Data Science! I can:

1. **Create a structured curriculum** - Tell me "teach me data science"
2. **Find learning resources** - Ask me "find data analysis resources"
3. **Explain concepts deeply** - Say "explain statistics concepts"

**Available Learning Areas:**
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

What would you like me to help you with?
                    """
                else:
                    response = f"""
I understand you want to learn about: "{item.text}"

I can help you with comprehensive learning support for:

• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

**How I can help:**
1. **Create structured curricula** - "Teach me [domain]"
2. **Find learning resources** - "Find [topic] resources"
3. **Explain concepts deeply** - "Explain [concept]"

What would you like to learn about?
                    """
            
            response_message = create_text_chat(response)
            await ctx.send(sender, response_message)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_message = create_text_chat("""
**Thank you for learning with me!**

Remember:
• Learning is a journey, not a destination
• Take breaks and practice regularly
• Don't hesitate to ask questions
• Use all my capabilities: curriculum, resources, and deep insights

Happy learning!
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@learning_chat_proto.on_message(ChatAcknowledgement)
async def handle_learning_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

@learning_agent.on_message(model=Response)
async def handle_agent_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender} ({msg.agent_type}): {msg.message}")
    
    if hasattr(ctx, 'pending_responses'):
        ctx.pending_responses[sender] = msg.message
    else:
        ctx.pending_responses = {sender: msg.message}

@learning_agent.on_message(model=CurriculumResponse)
async def handle_curriculum_response(ctx: Context, sender: str, msg: CurriculumResponse):
    ctx.logger.info(f"Received curriculum response from {sender}")
    
    if msg.success:
        ctx.logger.info("Curriculum generated successfully")
        
        original_sender = pending_requests.get(msg.request_id)
        
        if original_sender:
            try:
                response_message = create_text_chat(msg.curriculum)
                await ctx.send(original_sender, response_message)
                ctx.logger.info(f"Sent curriculum response to user {original_sender}")
                del pending_requests[msg.request_id]
            except Exception as e:
                ctx.logger.error(f"Failed to send curriculum response: {e}")
        else:
            ctx.logger.warning(f"No original sender found for request_id: {msg.request_id}")
    else:
        ctx.logger.error(f"Curriculum generation failed: {msg.error}")
        original_sender = pending_requests.get(msg.request_id)
        
        if original_sender:
            try:
                error_message = create_text_chat(f"Sorry, I couldn't generate the curriculum. Error: {msg.error}")
                await ctx.send(original_sender, error_message)
                del pending_requests[msg.request_id]
            except Exception as e:
                ctx.logger.error(f"Failed to send error response: {e}")

@learning_agent.on_message(model=MaterialsResponse)
async def handle_materials_response(ctx: Context, sender: str, msg: MaterialsResponse):
    ctx.logger.info(f"Received materials response from {sender}")
    
    if msg.success:
        ctx.logger.info("Materials generated successfully")
        full_response = msg.materials + msg.youtube_videos
        
        original_sender = pending_requests.get(msg.request_id)
        
        if original_sender:
            try:
                response_message = create_text_chat(full_response)
                await ctx.send(original_sender, response_message)
                ctx.logger.info(f"Sent materials response to user {original_sender}")
                del pending_requests[msg.request_id]
            except Exception as e:
                ctx.logger.error(f"Failed to send materials response: {e}")
        else:
            ctx.logger.warning(f"No original sender found for request_id: {msg.request_id}")
    else:
        ctx.logger.error(f"Materials generation failed: {msg.error}")
        original_sender = pending_requests.get(msg.request_id)
        
        if original_sender:
            try:
                error_message = create_text_chat(f"Sorry, I couldn't find materials. Error: {msg.error}")
                await ctx.send(original_sender, error_message)
                del pending_requests[msg.request_id]
            except Exception as e:
                ctx.logger.error(f"Failed to send error response: {e}")

@learning_agent.on_message(model=InsightsResponse)
async def handle_insights_response(ctx: Context, sender: str, msg: InsightsResponse):
    ctx.logger.info(f"Received insights response from {sender}")
    
    if msg.success:
        ctx.logger.info("Insights generated successfully")
        
        original_sender = pending_requests.get(msg.request_id)
        
        if original_sender:
            try:
                response_message = create_text_chat(msg.insights)
                await ctx.send(original_sender, response_message)
                ctx.logger.info(f"Sent insights response to user {original_sender}")
                del pending_requests[msg.request_id]
            except Exception as e:
                ctx.logger.error(f"Failed to send insights response: {e}")
        else:
            ctx.logger.warning(f"No original sender found for request_id: {msg.request_id}")
    else:
        ctx.logger.error(f"Insights generation failed: {msg.error}")
        original_sender = pending_requests.get(msg.request_id)
        
        if original_sender:
            try:
                error_message = create_text_chat(f"Sorry, I couldn't generate insights. Error: {msg.error}")
                await ctx.send(original_sender, error_message)
                del pending_requests[msg.request_id]
            except Exception as e:
                ctx.logger.error(f"Failed to send error response: {e}")

learning_agent.include(learning_chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(learning_agent.wallet.address())
    
    print("Learning Path Agent System")
    print("=" * 50)
    print(f"Learning Path Agent: {learning_agent.address}")
    print(f"Agent Name: {AGENT_NAME}")
    print(f"Agent Description: {AGENT_DESCRIPTION}")
    print(f"Port: 8000")

    print("\nStarting Learning Path Agent...")
    
    learning_agent.run()