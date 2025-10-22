
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

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION, ENHANCED_AGENT_SEED
from services.gemini_service import GeminiLearningService
from models import InsightsRequest, InsightsResponse

enhanced_agent = Agent(
    name="EnhancedAgent",
    seed=ENHANCED_AGENT_SEED,
    port=8003,
    mailbox=True
)

enhanced_chat_proto = Protocol(spec=chat_protocol_spec)

gemini_service = GeminiLearningService()

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

@enhanced_chat_proto.on_message(ChatMessage)
async def handle_enhanced_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), 
        acknowledged_msg_id=msg.msg_id
    ))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_message = create_text_chat("""
**Welcome to Enhanced Learning Agent!**

I provide deep insights and intelligent analysis using dynamic AI for ANY domain.

**What makes me special:**
• **Dynamic Concept Analysis** - I explain how different topics connect and relate
• **AI-Powered Prerequisite Mapping** - I know what you need to learn using MeTTa knowledge graph
• **Intelligent Learning Sequence** - I suggest optimal order using AI analysis
• **Cross-Domain Connections** - I show how concepts relate across different fields
• **Deep AI Insights** - Powered by Gemini AI and MeTTa knowledge graph

**Unlimited Domain Support:**
• **Technology**: Programming, AI, Web3, Data Science, DevOps, Cybersecurity
• **Creative Arts**: Design, Music, Art, Photography, Creative Writing
• **Sciences**: Physics, Chemistry, Biology, Mathematics, Research Methods
• **Languages**: English, Spanish, French, Linguistics, Grammar
• **Life Skills**: Cooking, Fitness, Psychology, Philosophy, History
• **Business**: Marketing, Finance, Management, Entrepreneurship
• **And ANYTHING else you want to understand!**

**Try asking me ANYTHING:**
- "Explain quantum physics concepts"
- "How do cooking and chemistry relate?"
- "What should I learn first for philosophy?"
- "Explain the relationship between music and mathematics"

What would you like to understand deeply?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            print(f"[ENHANCED AGENT] Processing request: {item.text[:50]}...")
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
            if any(greeting in item.text.lower() for greeting in greeting_words):
                greeting_response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="enhanced_greeting",
                    user_id=sender
                )
                response_message = create_text_chat(greeting_response)
                await ctx.send(sender, response_message)
            else:
                concept = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                print(f"[ENHANCED AGENT] Generating insights for concept: {concept}, domain: {domain}")
                response = await gemini_service.generate_deep_insights(concept, domain, item.text)
                
                print(f"[ENHANCED AGENT] Insights generated, sending response...")
                response_message = create_text_chat(response)
                await ctx.send(sender, response_message)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_message = create_text_chat("""
**Thank you for learning with me!**

**Remember:**
• Understanding concept relationships accelerates learning
• Prerequisites provide the foundation for advanced topics
• Practice and application reinforce theoretical knowledge
• Connect with our other agents for comprehensive learning support

Happy learning!
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@enhanced_chat_proto.on_message(ChatAcknowledgement)
async def handle_enhanced_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

@enhanced_agent.on_message(model=InsightsRequest)
async def handle_insights_request(ctx: Context, sender: str, msg: InsightsRequest):
    ctx.logger.info(f"Received insights request from {sender}: {msg.concept} in {msg.domain}")
    
    try:
        insights = await gemini_service.generate_deep_insights(msg.concept, msg.domain, msg.user_query)
        await ctx.send(sender, InsightsResponse(
            insights=insights,
            success=True,
            request_id=msg.request_id
        ))
        ctx.logger.info(f"Sent insights response to {sender}")
    except Exception as e:
        ctx.logger.error(f"Error generating insights: {e}")
        await ctx.send(sender, InsightsResponse(
            insights="",
            success=False,
            error=str(e),
            request_id=msg.request_id
        ))

enhanced_agent.include(enhanced_chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(enhanced_agent.wallet.address())
    
    print("Enhanced Learning Agent System")
    print("=" * 50)
    print(f"Enhanced Agent: {enhanced_agent.address}")
    print(f"Agent Name: EnhancedAgent")
    print(f"Port: 8003")
    print("\nStarting Enhanced Learning Agent...")
    
    enhanced_agent.run()
