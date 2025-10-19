
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
    
    words = query_lower.split()
    
    for i in range(len(words) - 1):
        two_word = f"{words[i]}_{words[i+1]}"
        if len(two_word) > 6:
            return two_word
    
    for word in words:
        if len(word) > 3 and word not in ["the", "and", "for", "with", "from", "that", "this", "will", "learn", "teach", "help", "want", "need"]:
            return word
    
    return query_lower.replace(" ", "_")

def _extract_domain_from_query(query: str) -> str:
    query_lower = query.lower()
    
    domain_keywords = {
        "programming": ["code", "program", "software", "development", "coding", "python", "javascript", "java", "c++", "c#", "go", "rust"],
        "data_science": ["data", "analysis", "statistics", "machine learning", "ai", "pandas", "numpy", "analytics", "big data"],
        "web_development": ["web", "frontend", "backend", "full stack", "react", "vue", "angular", "nodejs", "javascript", "html", "css"],
        "mobile_development": ["mobile", "app", "ios", "android", "swift", "kotlin", "react native", "flutter"],
        "devops": ["devops", "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "infrastructure", "deployment"],
        "cybersecurity": ["cybersecurity", "security", "hacking", "penetration", "cyber", "ethical hacking", "network security"],
        "design": ["design", "ui", "ux", "figma", "adobe", "user interface", "user experience", "visual design"],
        "business": ["business", "marketing", "finance", "management", "entrepreneurship", "strategy"],
        "science": ["science", "physics", "chemistry", "biology", "math", "mathematics", "research"],
        "language": ["language", "english", "spanish", "french", "learning", "grammar", "linguistics"],
        "music": ["music", "guitar", "piano", "singing", "composition", "audio", "sound"],
        "art": ["art", "drawing", "painting", "sculpture", "digital art", "photography"],
        "cooking": ["cooking", "baking", "culinary", "recipe", "chef", "food"],
        "fitness": ["fitness", "exercise", "workout", "gym", "yoga", "running", "training"],
        "psychology": ["psychology", "mental health", "therapy", "counseling", "behavior"],
        "philosophy": ["philosophy", "ethics", "logic", "metaphysics", "thinking"],
        "history": ["history", "historical", "ancient", "medieval", "modern", "world history"],
        "literature": ["literature", "writing", "poetry", "novel", "creative writing", "reading"]
    }
    
    for domain, keywords in domain_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            return domain
    
    return "general"

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
**Welcome to EduFinder - Your Unlimited AI Learning Companion!**

I'm your dynamic learning assistant powered by **MeTTa Knowledge Graph** and **Gemini AI** that can handle ANY educational topic or domain!

**What I can help you with:**
• **Dynamic Curriculum Creation** - AI-powered learning paths for ANY subject
• **Intelligent Resource Discovery** - Real-time educational content discovery
• **Deep Conceptual Insights** - Advanced reasoning and concept relationships
• **Unlimited Domain Support** - From programming to philosophy, cooking to quantum physics!

**Supported Learning Domains (Unlimited!):**
• **Technology**: Programming, AI, Web3, Data Science, DevOps, Cybersecurity
• **Creative Arts**: Design, Music, Art, Photography, Creative Writing
• **Sciences**: Physics, Chemistry, Biology, Mathematics, Research Methods
• **Languages**: English, Spanish, French, Linguistics, Grammar
• **Life Skills**: Cooking, Fitness, Psychology, Philosophy, History
• **Business**: Marketing, Finance, Management, Entrepreneurship
• **And ANYTHING else you want to learn!**

**Powered by Advanced AI:**
• **MeTTa Knowledge Graph** - Dynamic concept analysis and relationships
• **Gemini AI** - Natural language understanding and generation
• **Real-time Learning** - Adapts to any topic instantly
• **Intelligent Reasoning** - Deep insights and personalized guidance

**Try asking me ANYTHING:**
- "Teach me quantum physics" (curriculum creation)
- "Find resources for learning Spanish" (resource discovery)  
- "Explain the philosophy of ethics" (deep insights)
- "Create a learning path for cooking Italian cuisine"
- "Help me understand machine learning algorithms"
- "I want to learn guitar from scratch"

**No limits, no boundaries - just pure learning power!**

What would you like to learn today?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            user_input = item.text.lower()
            
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
            if any(greeting in user_input for greeting in greeting_words):
                greeting_response = """
Hello! Welcome to EduFinder - Your AI-Powered Learning Companion!

I'm your comprehensive learning assistant that can help you with:

**Curriculum Creation** - Structured learning paths for any tech domain
**Resource Discovery** - Educational videos, courses, books, and projects with links  
**Deep Insights** - Concept relationships and learning dependencies

I work with specialized AI agents to provide you with personalized educational experiences. Just tell me what you want to learn about, and I'll route your request to the right specialist!

What would you like to learn today?
                """
                response_message = create_text_chat(greeting_response)
                await ctx.send(sender, response_message)
            elif any(keyword in user_input for keyword in ["teach me", "learn", "educational plan", "learning plan", "study plan", "curriculum", "learning path", "create a", "help me learn"]):
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
                response = f"Creating your comprehensive educational plan for {topic.replace('_', ' ').title()}..."
                
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
                response = f"Finding targeted resources for {topic.replace('_', ' ').title()}..."
                
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
                response = f"Generating deep insights about {concept.replace('_', ' ').title()}..."
                
            elif "help" in user_input or "what can you do" in user_input:
                response = """
**I'm your comprehensive Learning Path Agent!**

**My Capabilities:**

**Educational Plan Creation** - I create complete learning paths with step-by-step resources
**Resource Discovery** - I find targeted learning materials, courses, and videos
**Deep Insights** - I explain concepts, relationships, and learning dependencies
**Personalized Learning** - I adapt plans to your skill level and goals

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