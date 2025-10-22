
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

I specialize in creating structured learning paths and curricula for ANY domain using dynamic AI analysis.

**What I can help you with:**
• **Dynamic Curriculum Creation** - AI-powered learning paths for ANY subject
• **Intelligent Module Organization** - Break down complex subjects dynamically
• **Prerequisite Identification** - AI-powered dependency analysis
• **Learning Sequence Planning** - Optimal order using MeTTa knowledge graph
• **Difficulty Progression** - Adaptive difficulty based on concept complexity

**Unlimited Domain Support:**
• **Technology**: Programming, AI, Web3, Data Science, DevOps, Cybersecurity
• **Creative Arts**: Design, Music, Art, Photography, Creative Writing
• **Sciences**: Physics, Chemistry, Biology, Mathematics, Research Methods
• **Languages**: English, Spanish, French, Linguistics, Grammar
• **Life Skills**: Cooking, Fitness, Psychology, Philosophy, History
• **Business**: Marketing, Finance, Management, Entrepreneurship
• **And ANYTHING else you want to learn!**

**Try asking me ANYTHING:**
- "Teach me quantum physics"
- "Create a cooking curriculum"
- "What should I learn first for philosophy?"
- "Make a learning path for guitar"

What would you like to learn about?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            print(f"[CURRICULUM AGENT] Processing request: {item.text[:50]}...")
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
            if any(greeting in item.text.lower() for greeting in greeting_words):
                greeting_response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="curriculum_greeting",
                    user_id=sender
                )
                response_message = create_text_chat(greeting_response)
                await ctx.send(sender, response_message)
            else:
                print(f"[CURRICULUM AGENT] Generating curriculum using Gemini + MeTTa...")
                response = await gemini_service.generate_curriculum("general", item.text, sender)
                
                print(f"[CURRICULUM AGENT] Curriculum generated, sending response...")
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
        curriculum = await gemini_service.generate_curriculum(msg.domain, msg.user_query, msg.original_sender)
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
