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

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent())
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content
    )

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
**Welcome to Learning Path Agent!**

I'm your comprehensive AI learning companion that creates personalized curricula, discovers educational resources, and provides deep insights through knowledge graph integration.

**What I can help you with:**
• **Curriculum Creation** - Structured learning paths for various domains
• **Resource Discovery** - Educational videos, courses, books, and projects
• **Deep Insights** - Concept relationships and learning dependencies via MeTTa
• **Personalized Learning** - Adapts to your skill level and goals

**Available Learning Domains:**
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

**Try asking me:**
- "Teach me AI engineering" (curriculum creation)
- "Find machine learning resources" (resource discovery)
- "Explain deep learning concepts" (deep insights)
- "Create a personalized learning path"

What would you like to learn today?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            user_input = item.text.lower()
            
            if any(keyword in user_input for keyword in ["curriculum", "teach me", "learning path", "create a"]):
                domain = "ai_engineering"
                if "web3" in user_input or "blockchain" in user_input or "smart contract" in user_input:
                    domain = "web3_development"
                elif "data science" in user_input or "data analysis" in user_input or "statistics" in user_input:
                    domain = "data_science"
                
                await ctx.send(CURRICULUM_AGENT_ADDRESS, CurriculumRequest(
                    domain=domain,
                    user_query=item.text
                ))
                response = f"📚 Routing your curriculum request to the Curriculum Agent for {domain.replace('_', ' ').title()}..."
                
            elif any(keyword in user_input for keyword in ["resources", "find", "get me", "show me", "videos", "courses", "books"]):
                topic = "machine learning"
                domain = "ai_engineering"
                
                if "deep learning" in user_input or "neural network" in user_input:
                    topic = "deep learning"
                elif "blockchain" in user_input:
                    topic = "blockchain"
                    domain = "web3_development"
                elif "smart contract" in user_input or "solidity" in user_input:
                    topic = "smart contracts"
                    domain = "web3_development"
                elif "data analysis" in user_input or "pandas" in user_input:
                    topic = "data analysis"
                    domain = "data_science"
                elif "statistics" in user_input or "statistical" in user_input:
                    topic = "statistics"
                    domain = "data_science"
                
                await ctx.send(MATERIALS_AGENT_ADDRESS, MaterialsRequest(
                    topic=topic,
                    domain=domain,
                    include_youtube="youtube" in user_input or "videos" in user_input
                ))
                response = f"🎥 Routing your materials request to the Materials Agent for {topic} in {domain.replace('_', ' ').title()}..."
                
            elif any(keyword in user_input for keyword in ["explain", "how does", "what is", "concept", "relationship", "prerequisite"]):
                concept = "machine learning"
                domain = "ai_engineering"
                
                if "deep learning" in user_input:
                    concept = "deep learning"
                elif "blockchain" in user_input:
                    concept = "blockchain"
                    domain = "web3_development"
                elif "smart contract" in user_input:
                    concept = "smart contracts"
                    domain = "web3_development"
                elif "data science" in user_input or "data analysis" in user_input:
                    concept = "data science"
                    domain = "data_science"
                elif "statistics" in user_input:
                    concept = "statistics"
                    domain = "data_science"
                
                await ctx.send(ENHANCED_AGENT_ADDRESS, InsightsRequest(
                    concept=concept,
                    domain=domain,
                    query_type="explain"
                ))
                response = f"🧠 Routing your insights request to the Enhanced Agent for {concept} in {domain.replace('_', ' ').title()}..."
                    
            elif "help" in user_input or "what can you do" in user_input:
                response = """
**I'm your comprehensive Learning Path Agent!**

**My Capabilities:**

**Curriculum Creation** - I create structured learning paths for various technical domains
**Resource Discovery** - I find educational videos, courses, books, and hands-on projects
**Deep Insights** - I understand concept relationships and learning dependencies via MeTTa knowledge graph
**Personalized Learning** - I adapt to your skill level and learning preferences

**Try asking me:**
- "Teach me AI engineering" (curriculum)
- "Find machine learning resources" (resources)
- "Explain deep learning concepts" (insights)
- "Create a personalized learning path" (comprehensive)

**Available Domains:**
• AI Engineering - Machine learning, deep learning, neural networks
• Web3 Development - Blockchain, smart contracts, DApps
• Data Science - Data analysis, statistics, machine learning

What would you like to learn?
                """
            else:
                # General response - try to determine intent
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
        if hasattr(ctx, 'pending_responses'):
            ctx.pending_responses[sender] = msg.curriculum
        else:
            ctx.pending_responses = {sender: msg.curriculum}
    else:
        ctx.logger.error(f"Curriculum generation failed: {msg.error}")

@learning_agent.on_message(model=MaterialsResponse)
async def handle_materials_response(ctx: Context, sender: str, msg: MaterialsResponse):
    ctx.logger.info(f"Received materials response from {sender}")
    
    if msg.success:
        ctx.logger.info("Materials generated successfully")
        full_response = msg.materials + msg.youtube_videos
        if hasattr(ctx, 'pending_responses'):
            ctx.pending_responses[sender] = full_response
        else:
            ctx.pending_responses = {sender: full_response}
    else:
        ctx.logger.error(f"Materials generation failed: {msg.error}")

@learning_agent.on_message(model=InsightsResponse)
async def handle_insights_response(ctx: Context, sender: str, msg: InsightsResponse):
    ctx.logger.info(f"Received insights response from {sender}")
    
    if msg.success:
        ctx.logger.info("Insights generated successfully")
        if hasattr(ctx, 'pending_responses'):
            ctx.pending_responses[sender] = msg.insights
        else:
            ctx.pending_responses = {sender: msg.insights}
    else:
        ctx.logger.error(f"Insights generation failed: {msg.error}")

learning_agent.include(learning_chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(learning_agent.wallet.address())
    
    print("Learning Path Agent System")
    print("=" * 50)
    print(f"Learning Path Agent: {learning_agent.address}")
    print(f"Agent Name: {AGENT_NAME}")
    print(f"Agent Description: {AGENT_DESCRIPTION}")
    print(f"Port: 8000")
    print("\nAgent Seeds Configuration:")
    print(f"• Main Agent Seed: {AGENT_SEED}")
    print(f"• Curriculum Agent Seed: {CURRICULUM_AGENT_SEED}")
    print(f"• Materials Agent Seed: {MATERIALS_AGENT_SEED}")
    print(f"• Enhanced Agent Seed: {ENHANCED_AGENT_SEED}")
    print("\nStarting Learning Path Agent...")
    
    learning_agent.run()