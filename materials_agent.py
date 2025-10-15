from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional
import json
import asyncio
import aiohttp

try:
    from youtubesearchpython import VideosSearch
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION

materials_agent = Agent(
    name="LearningMaterialsAgent",
    seed=AGENT_SEED + "_materials"
)

chat_proto = Protocol(spec=chat_protocol_spec)

LEARNING_RESOURCES = {
    "ai_engineering": {
        "foundations": {
            "videos": [
                "Machine Learning Crash Course by Google",
                "Introduction to Artificial Intelligence by MIT",
                "Linear Algebra for Machine Learning",
                "Statistics for Data Science"
            ],
            "courses": [
                "Coursera: Machine Learning by Andrew Ng",
                "edX: Introduction to Artificial Intelligence",
                "Udacity: Intro to Machine Learning"
            ],
            "books": [
                "Pattern Recognition and Machine Learning by Christopher Bishop",
                "The Elements of Statistical Learning by Hastie, Tibshirani, Friedman"
            ],
            "projects": [
                "Build a Linear Regression Model from Scratch",
                "Implement K-Means Clustering",
                "Create a Simple Neural Network"
            ]
        },
        "deep_learning": {
            "videos": [
                "Deep Learning Specialization by Andrew Ng",
                "Neural Networks and Deep Learning by 3Blue1Brown",
                "Convolutional Neural Networks Explained",
                "Recurrent Neural Networks Tutorial"
            ],
            "courses": [
                "Deep Learning Specialization - Coursera",
                "Fast.ai Practical Deep Learning",
                "CS231n: Convolutional Neural Networks - Stanford"
            ],
            "books": [
                "Deep Learning by Ian Goodfellow",
                "Hands-On Machine Learning by Aurélien Géron"
            ],
            "projects": [
                "Image Classification with CNN",
                "Text Generation with RNN",
                "Build a Chatbot with Transformers"
            ]
        },
        "ai_engineering": {
            "videos": [
                "MLOps: Machine Learning Operations",
                "Model Deployment Best Practices",
                "AI Ethics and Responsible AI",
                "Production Machine Learning Systems"
            ],
            "courses": [
                "MLOps Specialization - Coursera",
                "Machine Learning Engineering for Production - DeepLearning.AI",
                "AWS Machine Learning Specialty"
            ],
            "books": [
                "Designing Machine Learning Systems by Chip Huyen",
                "Building Machine Learning Powered Applications by Emmanuel Ameisen"
            ],
            "projects": [
                "Deploy ML Model to Cloud",
                "Build ML Pipeline with MLOps",
                "Create AI Ethics Framework"
            ]
        }
    },
    "web3_development": {
        "blockchain_fundamentals": {
            "videos": [
                "Blockchain Explained by Simply Explained",
                "How Bitcoin Works by 3Blue1Brown",
                "Ethereum Explained by Finematics",
                "Smart Contracts Tutorial"
            ],
            "courses": [
                "Blockchain Basics - Coursera",
                "Ethereum Development Course - freeCodeCamp",
                "Web3 Development Bootcamp"
            ],
            "books": [
                "Mastering Ethereum by Andreas Antonopoulos",
                "Programming Bitcoin by Jimmy Song"
            ],
            "projects": [
                "Build Your First Smart Contract",
                "Create a Simple DApp",
                "Implement a Token Contract"
            ]
        },
        "smart_contracts": {
            "videos": [
                "Solidity Tutorial for Beginners",
                "Smart Contract Security Best Practices",
                "DeFi Protocol Development",
                "NFT Development Tutorial"
            ],
            "courses": [
                "Solidity Course - CryptoZombies",
                "Ethereum Developer Bootcamp",
                "DeFi Development Course"
            ],
            "books": [
                "Solidity Programming Essentials by Ritesh Modi",
                "DeFi and the Future of Finance by Campbell Harvey"
            ],
            "projects": [
                "Build a DeFi Lending Protocol",
                "Create an NFT Marketplace",
                "Develop a DAO Governance System"
            ]
        }
    },
    "data_science": {
        "data_analysis": {
            "videos": [
                "Python for Data Science by freeCodeCamp",
                "Pandas Tutorial by Corey Schafer",
                "Data Visualization with Matplotlib",
                "Statistics for Data Science"
            ],
            "courses": [
                "Data Science Specialization - Coursera",
                "Python for Data Science - IBM",
                "Data Analysis with Python - freeCodeCamp"
            ],
            "books": [
                "Python for Data Analysis by Wes McKinney",
                "The Art of Data Science by Roger Peng"
            ],
            "projects": [
                "Analyze COVID-19 Dataset",
                "Build a Data Dashboard",
                "Create a Recommendation System"
            ]
        },
        "machine_learning": {
            "videos": [
                "Machine Learning Course by Andrew Ng",
                "Scikit-learn Tutorial",
                "Feature Engineering Techniques",
                "Model Evaluation and Validation"
            ],
            "courses": [
                "Machine Learning Course - Stanford",
                "Applied Data Science with Python - Coursera",
                "Machine Learning Bootcamp"
            ],
            "books": [
                "Introduction to Statistical Learning by James, Witten, Hastie, Tibshirani",
                "Python Machine Learning by Sebastian Raschka"
            ],
            "projects": [
                "Predict House Prices",
                "Build a Spam Classifier",
                "Create a Customer Segmentation Model"
            ]
        }
    }
}

async def search_youtube_videos(topic: str, max_results: int = 5) -> List[Dict[str, str]]:
    if not YOUTUBE_AVAILABLE:
        return []
    
    try:
        videosSearch = VideosSearch(topic, limit=max_results)
        results = videosSearch.result()
        
        videos = []
        for video in results.get('result', []):
            videos.append({
                "title": video.get("title", ""),
                "url": video.get("link", ""),
                "duration": video.get("duration", ""),
                "views": video.get("viewCount", {}).get("text", ""),
                "channel": video.get("channel", {}).get("name", "")
            })
        
        return videos
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

def format_learning_resources(domain: str, module: str, videos: List[Dict[str, str]]) -> str:
    static_resources = LEARNING_RESOURCES.get(domain, {}).get(module, {})
    
    response = f"""
**Learning Resources for {module.replace('_', ' ').title()}**

**Recommended Videos:**
"""
    
    for video in static_resources.get("videos", []):
        response += f"• {video}\n"
    
    if videos:
        response += "\n**Latest YouTube Videos:**\n"
        for video in videos[:3]:
            response += f"• [{video['title']}]({video['url']})\n"
            response += f"  {video['channel']} | {video['duration']} | {video['views']}\n"
    
    if static_resources.get("courses"):
        response += "\n**Online Courses:**\n"
        for course in static_resources["courses"]:
            response += f"• {course}\n"
    
    if static_resources.get("books"):
        response += "\n📖 **Recommended Books:**\n"
        for book in static_resources["books"]:
            response += f"• {book}\n"
    
    if static_resources.get("projects"):
        response += "\n🛠️ **Hands-on Projects:**\n"
        for project in static_resources["projects"]:
            response += f"• {project}\n"
    
    response += """
**Learning Tips:**
• Start with the fundamentals before moving to advanced topics
• Practice with hands-on projects
• Join online communities and forums
• Build a portfolio of your work
• Don't hesitate to ask questions!

Would you like me to:
1. Get more specific resources for a particular topic?
2. Suggest a learning schedule?
3. Connect you with study groups or communities?
"""
    
    return response

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(), 
        acknowledged_msg_id=msg.msg_id
    ))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_message = create_text_chat("""
**Welcome to Learning Materials Agent!**

I'm your educational resource specialist that finds the best learning materials for your journey.

**What I can help you with:**
• Find relevant YouTube videos and tutorials
• Recommend online courses and books
• Suggest hands-on projects
• Provide learning schedules and tips
• Connect you with educational communities

**How to get started:**
Tell me what specific topic or module you'd like resources for! For example:
- "Get me resources for AI engineering foundations"
- "Find videos about deep learning"
- "I need materials for Web3 smart contracts"

What would you like to learn about?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            user_input = item.text.lower()
            
            domain = None
            module = None
            
            if "ai engineering" in user_input or "artificial intelligence" in user_input:
                domain = "ai_engineering"
                if "foundation" in user_input or "basic" in user_input:
                    module = "foundations"
                elif "deep learning" in user_input:
                    module = "deep_learning"
                elif "engineering" in user_input or "production" in user_input:
                    module = "ai_engineering"
                else:
                    module = "foundations"
                    
            elif "web3" in user_input or "blockchain" in user_input:
                domain = "web3_development"
                if "fundamental" in user_input or "basic" in user_input:
                    module = "blockchain_fundamentals"
                elif "smart contract" in user_input:
                    module = "smart_contracts"
                else:
                    module = "blockchain_fundamentals"
                    
            elif "data science" in user_input:
                domain = "data_science"
                if "analysis" in user_input or "pandas" in user_input:
                    module = "data_analysis"
                elif "machine learning" in user_input:
                    module = "machine_learning"
                else:
                    module = "data_analysis"
            
            if domain and module:
                search_query = f"{domain.replace('_', ' ')} {module.replace('_', ' ')} tutorial"
                videos = await search_youtube_videos(search_query)
                
                response = format_learning_resources(domain, module, videos)
            elif "help" in user_input:
                response = """
**I can help you find learning resources for:**

🎯 **AI Engineering**
• Foundations of AI
• Deep Learning
• AI Engineering Practices

🌐 **Web3 Development**
• Blockchain Fundamentals
• Smart Contract Development
• DeFi and dApps

📊 **Data Science**
• Data Analysis
• Machine Learning
• Advanced Analytics

**Try asking me:**
- "Get me resources for AI engineering foundations"
- "Find videos about deep learning"
- "I need materials for Web3 smart contracts"
- "Show me data science tutorials"

What specific topic interests you?
                """
            else:
                response = f"""
I understand you're looking for resources about: "{item.text}"

I can help you find materials for:
• **AI Engineering** - Machine learning, deep learning, AI production systems
• **Web3 Development** - Blockchain, smart contracts, DeFi
• **Data Science** - Data analysis, machine learning, statistics

Please be more specific about which domain and topic you'd like resources for. For example:
- "Get me resources for AI engineering foundations"
- "Find videos about Web3 smart contracts"
- "Show me data science tutorials"

You can also ask me "help" to see all my capabilities!
                """
            
            response_message = create_text_chat(response)
            await ctx.send(sender, response_message)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_message = create_text_chat("""
**Happy Learning!**

Remember:
• Practice regularly with hands-on projects
• Join online communities for support
• Build a portfolio to showcase your skills
• Stay curious and keep exploring!

Good luck with your learning journey!
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

materials_agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(materials_agent.wallet.address())
    
    print(f"Learning Materials Agent address: {materials_agent.address}")
    print(f"Learning Materials Agent name: {materials_agent.name}")
    print("Starting Learning Materials Agent...")
    
    materials_agent.run()