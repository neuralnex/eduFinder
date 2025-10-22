
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

I specialize in discovering and providing educational resources with direct links for ANY domain using dynamic AI analysis.

**What I can help you with:**
• **Dynamic Resource Discovery** - Educational videos, courses, books, and projects with links
• **Intelligent YouTube Search** - Real-time educational content discovery
• **AI-Powered Learning Materials** - Curated resources using MeTTa insights
• **Project Suggestions** - Hands-on exercises and practical applications
• **Link Aggregation** - Direct links to courses, documentation, and tools

**Unlimited Domain Support:**
• **Technology**: Programming, AI, Web3, Data Science, DevOps, Cybersecurity
• **Creative Arts**: Design, Music, Art, Photography, Creative Writing
• **Sciences**: Physics, Chemistry, Biology, Mathematics, Research Methods
• **Languages**: English, Spanish, French, Linguistics, Grammar
• **Life Skills**: Cooking, Fitness, Psychology, Philosophy, History
• **Business**: Marketing, Finance, Management, Entrepreneurship
• **And ANYTHING else you want to learn!**

**Try asking me ANYTHING:**
- "Find quantum physics resources"
- "Get me cooking tutorials with videos"
- "Show me philosophy projects"
- "Find guitar learning materials"

What resources do you need?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            print(f"[MATERIALS AGENT] Processing request: {item.text[:50]}...")
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
            if any(greeting in item.text.lower() for greeting in greeting_words):
                greeting_response = await gemini_service.generate_conversational_response(
                    user_query=item.text,
                    context_type="materials_greeting",
                    user_id=sender
                )
                response_message = create_text_chat(greeting_response)
                await ctx.send(sender, response_message)
            else:
                topic = _extract_topic_from_query(item.text)
                domain = _extract_domain_from_query(item.text)
                print(f"[MATERIALS AGENT] Generating materials for topic: {topic}, domain: {domain}")
                response = await gemini_service.generate_learning_materials(topic, domain, item.text)
                
                print(f"[MATERIALS AGENT] Searching YouTube videos...")
                search_query = topic.replace("_", " ") + " tutorial"
                videos = await gemini_service.search_youtube_videos(search_query, 5)
                if videos:
                    response += "\n\n**🎥 Interactive Learning Videos:**\n"
                    for i, video in enumerate(videos, 1):
                        response += f"**{i}. {video['title']}**\n"
                        response += f"   📺 Channel: {video['channel']}\n"
                        response += f"   ⏱️ Duration: {video['duration']}\n"
                        response += f"   👀 Views: {video['views']}\n"
                        response += f"   📅 Published: {video['published']}\n"
                        response += f"   🔗 Watch: {video['url']}\n"
                        response += f"   🖼️ Thumbnail: {video['thumbnail']}\n"
                        if video.get('description'):
                            response += f"   📝 Description: {video['description']}\n"
                        response += "\n"
                    
                    response += "**💡 Practice-Focused Learning Resources:**\n"
                    response += "• **Hands-on Projects**: Build real applications as you learn\n"
                    response += "• **Interactive Coding**: Practice with live coding exercises\n"
                    response += "• **Project-Based Learning**: Learn by creating, not just reading\n"
                    response += "• **Community Practice**: Join coding communities for peer learning\n"
                    response += "• **Daily Practice**: Consistent practice beats intensive studying\n"
                
                print(f"[MATERIALS AGENT] Materials generated, sending response...")
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
                youtube_videos = "\n\n**🎥 Interactive Learning Videos:**\n"
                for i, video in enumerate(videos, 1):
                    youtube_videos += f"**{i}. {video['title']}**\n"
                    youtube_videos += f"   📺 Channel: {video['channel']}\n"
                    youtube_videos += f"   ⏱️ Duration: {video['duration']}\n"
                    youtube_videos += f"   👀 Views: {video['views']}\n"
                    youtube_videos += f"   📅 Published: {video['published']}\n"
                    youtube_videos += f"   🔗 Watch: {video['url']}\n"
                    youtube_videos += f"   🖼️ Thumbnail: {video['thumbnail']}\n"
                    if video.get('description'):
                        youtube_videos += f"   📝 Description: {video['description']}\n"
                    youtube_videos += "\n"
                
                youtube_videos += "**💡 Practice-Focused Learning Resources:**\n"
                youtube_videos += "• **Hands-on Projects**: Build real applications as you learn\n"
                youtube_videos += "• **Interactive Coding**: Practice with live coding exercises\n"
                youtube_videos += "• **Project-Based Learning**: Learn by creating, not just reading\n"
                youtube_videos += "• **Community Practice**: Join coding communities for peer learning\n"
                youtube_videos += "• **Daily Practice**: Consistent practice beats intensive studying\n"
        
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
