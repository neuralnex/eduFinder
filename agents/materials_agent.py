#!/usr/bin/env python3

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

from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION, MATERIALS_AGENT_SEED
from services.gemini_service import GeminiLearningService
from models import MaterialsRequest, MaterialsResponse

materials_agent = Agent(
    name="MaterialsAgent",
    seed=MATERIALS_AGENT_SEED,
    port=8002,
    mailbox=True
)

materials_chat_proto = Protocol(spec=chat_protocol_spec)

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

@materials_chat_proto.on_message(ChatMessage)
async def handle_materials_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), 
        acknowledged_msg_id=msg.msg_id
    ))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_message = create_text_chat("""
**Welcome to Materials Agent!**

I specialize in discovering and providing educational resources for your learning journey.

**What I can help you with:**
• **Resource Discovery** - Educational videos, courses, books, and projects
• **YouTube Search** - Real-time educational content discovery
• **Learning Materials** - Curated resources for specific topics
• **Project Suggestions** - Hands-on exercises and practical applications

**Available Learning Domains:**
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

**Try asking me:**
- "Find machine learning resources"
- "Get me blockchain tutorials"
- "Show me data science projects"

What resources do you need?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            user_input = item.text.lower()
            
            if any(keyword in user_input for keyword in ["resources", "find", "get me", "show me", "videos", "courses", "books"]):
                if "machine learning" in user_input or "ml" in user_input:
                    response = await gemini_service.generate_learning_materials("machine learning", "ai_engineering")
                elif "deep learning" in user_input or "neural network" in user_input:
                    response = await gemini_service.generate_learning_materials("deep learning", "ai_engineering")
                elif "blockchain" in user_input:
                    response = await gemini_service.generate_learning_materials("blockchain", "web3_development")
                elif "smart contract" in user_input or "solidity" in user_input:
                    response = await gemini_service.generate_learning_materials("smart contracts", "web3_development")
                elif "data analysis" in user_input or "pandas" in user_input:
                    response = await gemini_service.generate_learning_materials("data analysis", "data_science")
                elif "statistics" in user_input or "statistical" in user_input:
                    response = await gemini_service.generate_learning_materials("statistics", "data_science")
                else:
                    response = await gemini_service.generate_learning_materials("machine learning", "ai_engineering")
                
                # Add YouTube videos to the response
                if "youtube" in user_input or "videos" in user_input:
                    topic = user_input.replace("youtube", "").replace("videos", "").strip()
                    if not topic:
                        topic = "machine learning tutorial"
                    videos = await gemini_service.search_youtube_videos(topic, 3)
                    if videos:
                        response += "\n\n**Latest YouTube Videos:**\n"
                        for video in videos:
                            response += f"• {video['title']} - {video['channel']}\n"
                            response += f"  Duration: {video['duration']} | Views: {video['views']}\n"
                            response += f"  Link: {video['url']}\n\n"
            elif "youtube videos on" in user_input:
                query = user_input.replace("youtube videos on", "").strip()
                videos = await gemini_service.search_youtube_videos(query, 5)
                if videos:
                    response = f"**Latest YouTube Videos for '{query.title()}'**\n\n"
                    for video in videos:
                        response += f"• {video['title']} - {video['channel']}\n"
                        response += f"  Duration: {video['duration']} | Views: {video['views']}\n"
                        response += f"  Link: {video['url']}\n\n"
                else:
                    response = f"Sorry, I couldn't find any YouTube videos for '{query.title()}' or the API key is missing."
            elif "help" in user_input or "what can you do" in user_input:
                response = """
**I'm your Materials Specialist!**

**My Capabilities:**
• **Resource Discovery** - Educational videos, courses, books, and projects
• **YouTube Search** - Real-time educational content discovery
• **Learning Materials** - Curated resources for specific topics
• **Project Suggestions** - Hands-on exercises and practical applications

**Available Domains:**
• AI Engineering - Machine learning, deep learning, neural networks
• Web3 Development - Blockchain, smart contracts, DApps
• Data Science - Data analysis, statistics, machine learning

**Try asking me:**
- "Find machine learning resources"
- "Get me blockchain tutorials"
- "Show me data science projects"

What resources do you need?
                """
            else:
                response = f"""
I understand you're looking for resources about: "{item.text}"

I specialize in finding educational materials for:
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

**How I can help:**
1. **Find learning resources** - "Find [topic] resources"
2. **Get specific materials** - "Get me [subject] tutorials"
3. **Show projects** - "Show me [domain] projects"

What specific resources are you looking for?
                """
            
            response_message = create_text_chat(response)
            await ctx.send(sender, response_message)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_message = create_text_chat("""
**Happy Learning!**

Remember:
• Start with videos for conceptual understanding
• Follow along with hands-on projects
• Join online communities for support
• Practice regularly to reinforce learning

Good luck with your learning journey!
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@materials_chat_proto.on_message(ChatAcknowledgement)
async def handle_materials_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

@materials_agent.on_message(model=MaterialsRequest)
async def handle_materials_request(ctx: Context, sender: str, msg: MaterialsRequest):
    ctx.logger.info(f"Received materials request from {sender}: {msg.topic} in {msg.domain}")
    
    try:
        materials = await gemini_service.generate_learning_materials(msg.topic, msg.domain)
        youtube_videos = ""
        
        if msg.include_youtube:
            videos = await gemini_service.search_youtube_videos(f"{msg.topic} {msg.domain} tutorial", 3)
            if videos:
                youtube_videos = "\n\n**Latest YouTube Videos:**\n"
                for video in videos:
                    youtube_videos += f"• {video['title']} - {video['channel']}\n"
                    youtube_videos += f"  Duration: {video['duration']} | Views: {video['views']}\n"
                    youtube_videos += f"  Link: {video['url']}\n\n"
        
        await ctx.send(sender, MaterialsResponse(
            materials=materials,
            youtube_videos=youtube_videos,
            success=True
        ))
        ctx.logger.info(f"Sent materials response to {sender}")
    except Exception as e:
        ctx.logger.error(f"Error generating materials: {e}")
        await ctx.send(sender, MaterialsResponse(
            materials="",
            youtube_videos="",
            success=False,
            error=str(e)
        ))

materials_agent.include(materials_chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(materials_agent.wallet.address())
    
    print("Materials Agent System")
    print("=" * 50)
    print(f"Materials Agent: {materials_agent.address}")
    print(f"Agent Name: MaterialsAgent")
    print(f"Port: 8002")
    print("\nStarting Materials Agent...")
    
    materials_agent.run()
