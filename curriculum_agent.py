from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any
import json

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

agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED
)

chat_proto = Protocol(spec=chat_protocol_spec)

LEARNING_DOMAINS = {
    "ai_engineering": {
        "name": "AI Engineering",
        "description": "Complete path to becoming an AI Engineer",
        "prerequisites": ["Basic programming", "Mathematics fundamentals"],
        "duration": "6-12 months",
        "modules": [
            {
                "title": "Foundations of AI",
                "duration": "4-6 weeks",
                "topics": ["Machine Learning basics", "Statistics", "Linear Algebra"],
                "difficulty": "Beginner"
            },
            {
                "title": "Deep Learning Fundamentals",
                "duration": "6-8 weeks", 
                "topics": ["Neural Networks", "CNN", "RNN", "Transformers"],
                "difficulty": "Intermediate"
            },
            {
                "title": "AI Engineering Practices",
                "duration": "8-10 weeks",
                "topics": ["MLOps", "Model Deployment", "AI Ethics", "Production Systems"],
                "difficulty": "Advanced"
            },
            {
                "title": "Specialized Applications",
                "duration": "6-8 weeks",
                "topics": ["Computer Vision", "NLP", "Reinforcement Learning", "Generative AI"],
                "difficulty": "Advanced"
            }
        ]
    },
    "web3_development": {
        "name": "Web3 Development",
        "description": "Complete path to becoming a Web3 Developer",
        "prerequisites": ["JavaScript/TypeScript", "Blockchain basics"],
        "duration": "4-8 months",
        "modules": [
            {
                "title": "Blockchain Fundamentals",
                "duration": "3-4 weeks",
                "topics": ["Cryptocurrency", "Smart Contracts", "Consensus Mechanisms"],
                "difficulty": "Beginner"
            },
            {
                "title": "Smart Contract Development",
                "duration": "6-8 weeks",
                "topics": ["Solidity", "Ethereum", "Testing", "Deployment"],
                "difficulty": "Intermediate"
            },
            {
                "title": "DeFi and dApps",
                "duration": "6-8 weeks",
                "topics": ["DeFi Protocols", "Frontend Integration", "Web3 Libraries"],
                "difficulty": "Intermediate"
            },
            {
                "title": "Advanced Web3",
                "duration": "4-6 weeks",
                "topics": ["Layer 2", "Cross-chain", "NFTs", "DAO Development"],
                "difficulty": "Advanced"
            }
        ]
    },
    "data_science": {
        "name": "Data Science",
        "description": "Complete path to becoming a Data Scientist",
        "prerequisites": ["Statistics", "Programming basics"],
        "duration": "6-10 months",
        "modules": [
            {
                "title": "Data Analysis Fundamentals",
                "duration": "4-6 weeks",
                "topics": ["Python/R", "Pandas", "Data Visualization", "Statistics"],
                "difficulty": "Beginner"
            },
            {
                "title": "Machine Learning",
                "duration": "6-8 weeks",
                "topics": ["Supervised Learning", "Unsupervised Learning", "Model Evaluation"],
                "difficulty": "Intermediate"
            },
            {
                "title": "Advanced Analytics",
                "duration": "6-8 weeks",
                "topics": ["Time Series", "A/B Testing", "Feature Engineering"],
                "difficulty": "Intermediate"
            },
            {
                "title": "Production Data Science",
                "duration": "4-6 weeks",
                "topics": ["MLOps", "Big Data", "Cloud Platforms", "Business Intelligence"],
                "difficulty": "Advanced"
            }
        ]
    }
}

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

def generate_curriculum_response(domain: str, user_level: str = "beginner") -> str:
    if domain not in LEARNING_DOMAINS:
        available_domains = ", ".join(LEARNING_DOMAINS.keys())
        return f"Sorry, I don't have a curriculum for '{domain}'. Available domains: {available_domains}"
    
    domain_info = LEARNING_DOMAINS[domain]
    
    response = f"""
**{domain_info['name']} Learning Path**

**Overview**: {domain_info['description']}
**Duration**: {domain_info['duration']}
**Prerequisites**: {', '.join(domain_info['prerequisites'])}

**Learning Modules:**

"""
    
    for i, module in enumerate(domain_info['modules'], 1):
        response += f"""
**Module {i}: {module['title']}**
• Duration: {module['duration']}
• Difficulty: {module['difficulty']}
• Topics: {', '.join(module['topics'])}

"""
    
    response += """
**Next Steps**: 
I'll now connect you with our Learning Materials Agent to get specific resources, videos, and hands-on projects for each module!

Would you like me to:
1. Start with Module 1 and get learning materials?
2. Focus on a specific module?
3. Get an overview of all available resources?
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
**Welcome to Learning Path Agent!**

I'm your AI learning companion that creates personalized curricula and guides your educational journey.

**What I can help you with:**
• Create structured learning paths for various domains
• Break down complex topics into manageable modules
• Connect you with learning materials and resources
• Track your progress and suggest next steps

**Available Learning Domains:**
• AI Engineering
• Web3 Development  
• Data Science
• And more coming soon!

**How to get started:**
Just tell me what you'd like to learn! For example:
- "Teach me AI engineering"
- "I want to learn Web3 development"
- "Create a data science curriculum"

What would you like to learn today?
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            user_input = item.text.lower()
            
            if any(keyword in user_input for keyword in ["ai engineering", "ai engineer", "artificial intelligence"]):
                response = generate_curriculum_response("ai_engineering")
            elif any(keyword in user_input for keyword in ["web3", "blockchain", "smart contract", "defi"]):
                response = generate_curriculum_response("web3_development")
            elif any(keyword in user_input for keyword in ["data science", "data scientist", "machine learning"]):
                response = generate_curriculum_response("data_science")
            elif "help" in user_input or "what can you do" in user_input:
                response = """
**I can help you with:**

**Curriculum Creation**: I create structured learning paths for various technical domains
**Learning Materials**: I connect you with videos, tutorials, and hands-on projects
**Progress Tracking**: I help you stay on track and suggest next steps
**Personalized Learning**: I adapt to your skill level and learning preferences

**Try asking me:**
- "Teach me AI engineering"
- "I want to learn Web3 development" 
- "Create a data science curriculum"
- "What learning domains do you support?"

What would you like to learn?
                """
            else:
                response = f"""
I understand you want to learn about: "{item.text}"

I currently support these learning domains:
• **AI Engineering** - Complete path to becoming an AI Engineer
• **Web3 Development** - Blockchain and decentralized application development
• **Data Science** - Data analysis, machine learning, and analytics

Would you like me to create a curriculum for one of these domains, or would you like to suggest a new learning area?

You can also ask me "help" to see all my capabilities!
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
• Connect with our Learning Materials Agent for specific resources

Happy learning!
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(agent.wallet.address())
    
    print(f"Learning Path Agent address: {agent.address}")
    print(f"Learning Path Agent name: {agent.name}")
    print("Starting Learning Path Agent...")
    
    agent.run()