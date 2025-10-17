
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
            user_input = item.text.lower()
            
            if any(keyword in user_input for keyword in ["explain", "how does", "what is", "concept", "relationship", "prerequisite"]):
                if "ai" in user_input or "artificial intelligence" in user_input:
                    response = await gemini_service.generate_deep_insights("artificial intelligence", "ai_engineering")
                elif "machine learning" in user_input:
                    response = await gemini_service.generate_deep_insights("machine learning", "ai_engineering")
                elif "deep learning" in user_input:
                    response = await gemini_service.generate_deep_insights("deep learning", "ai_engineering")
                elif "web3" in user_input or "blockchain" in user_input:
                    response = await gemini_service.generate_deep_insights("blockchain", "web3_development")
                elif "smart contract" in user_input:
                    response = await gemini_service.generate_deep_insights("smart contracts", "web3_development")
                elif "data science" in user_input or "data analysis" in user_input:
                    response = await gemini_service.generate_deep_insights("data science", "data_science")
                elif "statistics" in user_input:
                    response = await gemini_service.generate_deep_insights("statistics", "data_science")
                else:
                    response = await gemini_service.generate_deep_insights("machine learning", "ai_engineering")
            elif "help" in user_input or "what can you do" in user_input:
                response = """
**I'm your Enhanced Learning Specialist!**

**My Special Capabilities:**
• **Deep Concept Analysis** - I understand how different topics connect and depend on each other
• **Prerequisite Mapping** - I know what you need to learn before tackling advanced topics
• **Learning Sequence Optimization** - I suggest the best order to learn concepts
• **Knowledge Graph Reasoning** - I use structured knowledge to provide intelligent insights
• **Cross-Domain Connections** - I show how concepts relate across different fields

**What I can help you with:**
• Explain complex concepts and their relationships
• Create personalized learning paths based on your goals
• Identify prerequisites and dependencies
• Suggest optimal learning sequences
• Connect concepts across different domains

**Try asking me:**
- "Explain how machine learning and deep learning relate"
- "What should I learn before studying neural networks?"
- "How do blockchain concepts connect?"

What would you like to understand deeply?
                """
            else:
                response = f"""
I understand you want to understand: "{item.text}"

I provide deep insights and analysis for:
• **AI Engineering** - Machine learning, deep learning, neural networks
• **Web3 Development** - Blockchain, smart contracts, DApps
• **Data Science** - Data analysis, statistics, machine learning

**How I can help:**
1. **Explain concepts deeply** - "Explain [concept]"
2. **Show relationships** - "How does [topic A] relate to [topic B]?"
3. **Identify prerequisites** - "What should I learn before [advanced topic]?"
4. **Optimize learning order** - "What's the best way to learn [domain]?"

What would you like me to analyze for you?
                """
            
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
