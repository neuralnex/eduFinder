
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

from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION, CURRICULUM_AGENT_SEED
from services.gemini_service import GeminiLearningService
from models import CurriculumRequest, CurriculumResponse

curriculum_agent = Agent(
    name="CurriculumAgent",
    seed=CURRICULUM_AGENT_SEED,
    port=8001,
    mailbox=True
)

curriculum_chat_proto = Protocol(spec=chat_protocol_spec)

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

@curriculum_chat_proto.on_message(ChatMessage)
async def handle_curriculum_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), 
        acknowledged_msg_id=msg.msg_id
    ))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_message = create_text_chat("""
**Welcome to Curriculum Agent!**

I specialize in creating structured learning paths and curricula for any technical domain using Gemini AI.

**What I can help you with:**
• **Curriculum Creation** - Structured learning paths for any tech domain
• **Learning Module Organization** - Break down complex subjects into manageable steps
• **Prerequisite Identification** - Show you what you need to learn first
• **Learning Sequence Planning** - Optimal order for mastering concepts
• **Difficulty Progression** - From beginner to advanced levels

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
• **And many more!** - I can create curricula for any educational domain

**Try asking me:**
- "Teach me React development"
- "Create a cybersecurity curriculum"
- "What should I learn first for machine learning?"
- "Make a learning path for DevOps"

What would you like to learn about?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            # Use Gemini to understand and respond to any query
            response = await gemini_service.generate_curriculum("general", item.text)
            
            response_message = create_text_chat(response)
            await ctx.send(sender, response_message)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_message = create_text_chat("""
**Thank you for learning with me!**

Remember:
• Start with fundamentals before advanced topics
• Practice regularly to reinforce learning
• Follow the structured learning path I provide
• Connect with our Materials Agent for specific resources

Happy learning!
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@curriculum_chat_proto.on_message(ChatAcknowledgement)
async def handle_curriculum_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

@curriculum_agent.on_message(model=CurriculumRequest)
async def handle_curriculum_request(ctx: Context, sender: str, msg: CurriculumRequest):
    ctx.logger.info(f"Received curriculum request from {sender}: {msg.domain}")
    
    try:
        curriculum = await gemini_service.generate_curriculum(msg.domain, msg.user_query)
        await ctx.send(sender, CurriculumResponse(
            curriculum=curriculum,
            success=True,
            request_id=msg.request_id
        ))
        ctx.logger.info(f"Sent curriculum response to {sender}")
    except Exception as e:
        ctx.logger.error(f"Error generating curriculum: {e}")
        await ctx.send(sender, CurriculumResponse(
            curriculum="",
            success=False,
            error=str(e),
            request_id=msg.request_id
        ))

curriculum_agent.include(curriculum_chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(curriculum_agent.wallet.address())
    
    print("Curriculum Agent System")
    print("=" * 50)
    print(f"Curriculum Agent: {curriculum_agent.address}")
    print(f"Agent Name: CurriculumAgent")
    print(f"Port: 8001")
    print("\nStarting Curriculum Agent...")
    
    curriculum_agent.run()
