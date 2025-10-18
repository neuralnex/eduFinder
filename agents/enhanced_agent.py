
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

I provide deep insights and intelligent analysis using Gemini AI for any technical domain.

**What makes me special:**
• **Deep Concept Analysis** - I explain how different topics connect and relate
• **Prerequisite Mapping** - I know what you need to learn before tackling advanced topics
• **Learning Sequence Optimization** - I suggest the best order to learn concepts
• **Cross-Domain Connections** - I show how concepts relate across different fields
• **Intelligent Insights** - Powered by Gemini AI for comprehensive understanding

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
• **And many more!** - I can provide insights for any educational domain

**Try asking me:**
- "Explain machine learning concepts"
- "How do React and Node.js relate?"
- "What should I learn first for cybersecurity?"
- "Explain the relationship between Docker and Kubernetes"

What would you like to understand deeply?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            # Check for greetings and respond naturally
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
            if any(greeting in item.text.lower() for greeting in greeting_words):
                greeting_response = """
Hello! 👋 I'm the Enhanced Learning Agent, your AI-powered deep insights specialist!

I specialize in providing deep conceptual analysis and intelligent insights for any technical domain. I can explain how different concepts connect, identify prerequisites, and help you understand the relationships between various topics.

What would you like to understand deeply? I'm here to provide comprehensive insights and analysis!
                """
                response_message = create_text_chat(greeting_response)
                await ctx.send(sender, response_message)
            else:
                # Use Gemini to understand and respond to any query
                response = await gemini_service.generate_deep_insights("general", "general", item.text)
                
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
