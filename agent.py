
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
from services.user_context import user_context_manager
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
    print(f"[MAIN AGENT] Received message from {sender}")
    ctx.logger.info(f"Received message from {sender}")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), 
        acknowledged_msg_id=msg.msg_id
    ))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            
            user_context = user_context_manager.get_context(sender)
            user_context.session_count += 1
            user_context_manager.save_contexts()
            
            personalized_greeting = user_context_manager.get_personalized_greeting(sender)
            
            welcome_message = create_text_chat(f"""
{personalized_greeting}

**I'm EduFinder - Your Intelligent Learning Companion!**

I'm powered by **MeTTa Knowledge Graph** and **Gemini AI** and I remember our conversations to provide personalized learning experiences.

**What makes me special:**
• **I remember you** - Your learning level, preferences, and goals
• **Adaptive Learning** - Content adjusts to your skill level and pace
• **Conversational Intelligence** - I understand context and build on our previous discussions
• **Unlimited Domains** - From programming to philosophy, cooking to quantum physics!

**I can help you with:**
• **Personalized Curricula** - Learning paths tailored to your level and goals
• **Smart Resource Discovery** - Materials that match your learning style
• **Deep Conceptual Insights** - Understanding how topics connect and relate
• **Progress Tracking** - I remember what you've learned and what's next

**Just tell me:**
- What you want to learn
- Your current level (beginner/intermediate/advanced)
- Your learning goals
- Any specific preferences

I'll create a personalized learning experience just for you!

What would you like to learn today?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            print(f"[MAIN AGENT] Processing text message: {item.text[:50]}...")
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            user_input = item.text.lower()
            
            user_context = user_context_manager.get_context(sender)
            
            learning_level = user_context_manager.assess_learning_level(sender, item.text)
            learning_goals = user_context_manager.extract_learning_goals(sender, item.text)
            learning_duration = user_context_manager.extract_learning_duration(sender, item.text)
            practice_focus = user_context_manager.extract_practice_preferences(sender, item.text)
            time_commitment = user_context_manager.extract_time_commitment(sender, item.text)
            
            if learning_level != "unknown":
                user_context_manager.update_context(sender, learning_level=learning_level)
            
            if learning_goals:
                user_context_manager.update_context(sender, learning_goals=learning_goals)
            
            if learning_duration != "flexible":
                user_context_manager.update_context(sender, preferred_duration=learning_duration)
            
            if practice_focus:
                user_context_manager.update_context(sender, practice_focus=practice_focus)
            
            if time_commitment != "not specified":
                user_context_manager.update_context(sender, daily_time_commitment=time_commitment)
            
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings", "how are you", "how are you doing"]
            if any(greeting in user_input for greeting in greeting_words):
                response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="greeting",
                    user_id=sender
                )
            elif any(phrase in user_input for phrase in ["thank you", "thanks", "appreciate", "grateful"]):
                response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="gratitude",
                    user_id=sender
                )
            elif any(phrase in user_input for phrase in ["learning speed", "slow learner", "not good", "struggle", "difficult", "hard for me"]):
                user_context_manager.update_context(sender, preferences=user_context.preferences)
                user_context.preferences.pace = "slow"
                user_context_manager.save_contexts()
                
                response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="learning_pace",
                    user_id=sender
                )
            elif any(keyword in user_input for keyword in ["teach me", "learn", "educational plan", "learning plan", "study plan", "curriculum", "learning path", "create a", "help me learn"]):
                topic = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                
                user_context_manager.update_context(sender, current_topic=topic, current_domain=domain)
                
                conversational_response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="learning_request",
                    user_id=sender,
                    topic=topic,
                    domain=domain
                )
                
                import time
                request_id = f"educational_plan_{int(time.time())}_{topic}_{domain}"
                pending_requests[request_id] = sender
                
                print(f"[MAIN AGENT] Routing to CURRICULUM AGENT for topic: {topic}, domain: {domain}")
                await ctx.send(CURRICULUM_AGENT_ADDRESS, CurriculumRequest(
                    domain=domain,
                    user_query=item.text,
                    original_sender=sender,
                    request_id=request_id
                ))
                response = conversational_response
                
            elif any(keyword in user_input for keyword in ["resources", "find", "get me", "show me", "videos", "courses", "books", "tutorials", "materials"]):
                topic = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                
                user_context_manager.update_context(sender, current_topic=topic, current_domain=domain)
                
                adaptive_prefix = user_context_manager.get_adaptive_response_prefix(sender, topic.replace('_', ' '))
                
                import time
                request_id = f"materials_{int(time.time())}_{topic}_{domain}"
                pending_requests[request_id] = sender
                
                print(f"[MAIN AGENT] Routing to MATERIALS AGENT for topic: {topic}, domain: {domain}")
                await ctx.send(MATERIALS_AGENT_ADDRESS, MaterialsRequest(
                    topic=topic,
                    domain=domain,
                    user_query=item.text,
                    include_youtube="youtube" in user_input or "videos" in user_input,
                    original_sender=sender,
                    request_id=request_id
                ))
                response = f"{adaptive_prefix}Finding personalized resources for {topic.replace('_', ' ').title()} that match your learning style..."
                
            elif any(keyword in user_input for keyword in ["explain", "how does", "what is", "concept", "relationship", "prerequisite", "deep insights"]):
                concept = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                
                user_context_manager.update_context(sender, current_topic=concept, current_domain=domain)
                
                adaptive_prefix = user_context_manager.get_adaptive_response_prefix(sender, concept.replace('_', ' '))
                
                import time
                request_id = f"insights_{int(time.time())}_{concept}_{domain}"
                pending_requests[request_id] = sender
                
                print(f"[MAIN AGENT] Routing to ENHANCED AGENT for concept: {concept}, domain: {domain}")
                await ctx.send(ENHANCED_AGENT_ADDRESS, InsightsRequest(
                    concept=concept,
                    domain=domain,
                    query_type="explain",
                    user_query=item.text,
                    original_sender=sender,
                    request_id=request_id
                ))
                response = f"{adaptive_prefix}Generating deep insights about {concept.replace('_', ' ').title()} tailored to your understanding level..."
                
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
                response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="general",
                    user_id=sender
                )
            
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