
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

def _extract_topic_from_query(query: str) -> str:
    query_lower = query.lower()
    
    common_tech_topics = [
        "machine learning", "deep learning", "neural networks", "artificial intelligence",
        "blockchain", "smart contracts", "solidity", "ethereum", "web3",
        "data science", "data analysis", "statistics", "pandas", "numpy",
        "python", "javascript", "typescript", "react", "nodejs", "vue", "angular",
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

I specialize in discovering and providing educational resources with direct links for any technical domain.

**What I can help you with:**
• **Resource Discovery** - Educational videos, courses, books, and projects with links
• **YouTube Search** - Real-time educational content discovery with detailed info
• **Learning Materials** - Curated resources for specific topics
• **Project Suggestions** - Hands-on exercises and practical applications
• **Link Aggregation** - Direct links to courses, documentation, and tools

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
• **And many more!** - I can find resources for any educational domain

**Try asking me:**
- "Find React development resources"
- "Get me Python tutorials with videos"
- "Show me cybersecurity projects"
- "Find Docker learning materials"

What resources do you need?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            # Check for greetings and respond naturally
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
            if any(greeting in item.text.lower() for greeting in greeting_words):
                greeting_response = """
Hello! 👋 I'm the Materials Agent, your educational resource discovery specialist!

I specialize in finding and providing educational resources with direct links for any technical domain. I can discover YouTube videos, courses, books, documentation, and hands-on projects to help you learn effectively.

What resources do you need? Just tell me what you want to learn and I'll find the best materials for you!
                """
                response_message = create_text_chat(greeting_response)
                await ctx.send(sender, response_message)
            else:
                # Use Gemini to understand and respond to any query
                topic = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                response = await gemini_service.generate_learning_materials(topic, domain, item.text)
                
                # Always include YouTube videos for better learning experience
                search_query = topic.replace("_", " ") + " tutorial"
                videos = await gemini_service.search_youtube_videos(search_query, 5)
                if videos:
                    response += "\n\n**🎥 Latest YouTube Learning Resources:**\n"
                    for i, video in enumerate(videos, 1):
                        response += f"**{i}. {video['title']}**\n"
                        response += f"   📺 Channel: {video['channel']}\n"
                        response += f"   ⏱️ Duration: {video['duration']}\n"
                        response += f"   👀 Views: {video['views']}\n"
                        response += f"   📅 Published: {video['published']}\n"
                        response += f"   🔗 Watch: {video['url']}\n"
                        if video.get('description'):
                            response += f"   📝 Description: {video['description']}\n"
                        response += "\n"
                    
                    response += "**💡 Additional Learning Resources:**\n"
                    response += "• **Free Courses**: https://www.coursera.org/, https://www.edx.org/\n"
                    response += "• **Practice Platforms**: https://leetcode.com/, https://www.hackerrank.com/\n"
                    response += "• **Documentation**: https://docs.python.org/, https://developer.mozilla.org/\n"
                    response += "• **Community**: Reddit, Stack Overflow, Discord communities\n"
                
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
        materials = await gemini_service.generate_learning_materials(msg.topic, msg.domain, msg.user_query)
        youtube_videos = ""
        
        if msg.include_youtube:
            videos = await gemini_service.search_youtube_videos(f"{msg.topic} {msg.domain} tutorial", 5)
            if videos:
                youtube_videos = "\n\n**🎥 Latest YouTube Learning Resources:**\n"
                for i, video in enumerate(videos, 1):
                    youtube_videos += f"**{i}. {video['title']}**\n"
                    youtube_videos += f"   📺 Channel: {video['channel']}\n"
                    youtube_videos += f"   ⏱️ Duration: {video['duration']}\n"
                    youtube_videos += f"   👀 Views: {video['views']}\n"
                    youtube_videos += f"   📅 Published: {video['published']}\n"
                    youtube_videos += f"   🔗 Watch: {video['url']}\n"
                    if video.get('description'):
                        youtube_videos += f"   📝 Description: {video['description']}\n"
                    youtube_videos += "\n"
                
                youtube_videos += "**💡 Additional Learning Resources:**\n"
                youtube_videos += "• **Free Courses**: https://www.coursera.org/, https://www.edx.org/\n"
                youtube_videos += "• **Practice Platforms**: https://leetcode.com/, https://www.hackerrank.com/\n"
                youtube_videos += "• **Documentation**: https://docs.python.org/, https://developer.mozilla.org/\n"
                youtube_videos += "• **Community**: Reddit, Stack Overflow, Discord communities\n"
        
        await ctx.send(sender, MaterialsResponse(
            materials=materials,
            youtube_videos=youtube_videos,
            success=True,
            request_id=msg.request_id
        ))
        ctx.logger.info(f"Sent materials response to {sender}")
    except Exception as e:
        ctx.logger.error(f"Error generating materials: {e}")
        await ctx.send(sender, MaterialsResponse(
            materials="",
            youtube_videos="",
            success=False,
            error=str(e),
            request_id=msg.request_id
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
