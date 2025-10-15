from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any
import json
import asyncio

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

from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION
from agents.metta_integration import MeTTaKnowledgeGraph

enhanced_agent = Agent(
    name="EnhancedLearningAgent",
    seed=AGENT_SEED + "_enhanced"
)

chat_proto = Protocol(spec=chat_protocol_spec)

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

async def generate_enhanced_curriculum(domain: str, user_level: str = "beginner", specific_concept: str = None) -> str:
    async with MeTTaKnowledgeGraph() as metta:
        if specific_concept:
            concept_data = await metta.query_learning_concepts(domain, specific_concept)
            
            if concept_data:
                response = f"""
🧠 **Deep Dive: {concept_data.get('concept', specific_concept)}**

📖 **Definition**: {concept_data.get('definition', 'No definition available')}

📋 **Prerequisites**:
"""
                for prereq in concept_data.get('prerequisites', []):
                    response += f"• {prereq}\n"
                
                response += f"""
🔗 **Related Concepts**:
"""
                for related in concept_data.get('related_concepts', []):
                    response += f"• {related}\n"
                
                response += f"""
📚 **Learning Path**:
"""
                for i, step in enumerate(concept_data.get('learning_path', []), 1):
                    response += f"{i}. {step}\n"
                
                response += f"""
⏱️ **Estimated Time**: {concept_data.get('estimated_time', 'Not specified')}
🎯 **Difficulty Level**: {concept_data.get('difficulty_level', 'Not specified')}

💡 **Next Steps**: 
I can connect you with our Learning Materials Agent to get specific resources for each step in your learning path!
"""
            else:
                response = f"Sorry, I couldn't find detailed information about '{specific_concept}' in the knowledge graph. Let me suggest some general learning paths instead."
        else:
            response = f"""
🎓 **{domain.replace('_', ' ').title()} Learning Path**

I'm using our MeTTa Knowledge Graph to create a personalized curriculum for you!

"""
            
            foundational_concepts = {
                "ai_engineering": ["machine learning", "deep learning", "neural networks"],
                "web3_development": ["blockchain", "smart contracts", "cryptocurrency"],
                "data_science": ["data analysis", "statistics", "machine learning"]
            }
            
            concepts = foundational_concepts.get(domain, [])
            
            if concepts:
                learning_order = await metta.suggest_learning_order(domain, concepts)
                
                response += "📚 **Recommended Learning Sequence**:\n\n"
                
                for i, concept in enumerate(learning_order, 1):
                    concept_data = await metta.query_learning_concepts(domain, concept)
                    definition = concept_data.get('definition', 'Learn about this important concept')
                    
                    response += f"""
**Step {i}: {concept.replace('_', ' ').title()}**
• {definition}
• Difficulty: {concept_data.get('difficulty_level', 'Not specified')}
• Time: {concept_data.get('estimated_time', 'Not specified')}
"""
                
                response += """
🚀 **Personalized Recommendations**:
Based on your learning level and the knowledge graph analysis, I recommend:

1. **Start with the fundamentals** - Build a strong foundation
2. **Practice regularly** - Apply concepts through hands-on projects  
3. **Connect concepts** - Understand how different topics relate
4. **Track progress** - Monitor your learning journey

💡 **Ready to dive deeper?**
Tell me which specific concept you'd like to explore, and I'll provide:
• Detailed learning path
• Prerequisites and dependencies
• Related concepts to explore
• Connection to learning materials

What would you like to learn first? 🎯
"""
            else:
                response += "I'm still building knowledge about this domain. Let me connect you with our Learning Materials Agent for resources!"
        
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
🧠 **Welcome to Enhanced Learning Agent!**

I'm your AI learning companion powered by MeTTa Knowledge Graph technology!

**What makes me special:**
• 🧠 **Knowledge Graph Integration** - I understand concept relationships and dependencies
• 🎯 **Personalized Learning Paths** - I create curricula based on your skill level
• 🔗 **Concept Connections** - I show you how different topics relate to each other
• 📚 **Structured Learning** - I break down complex subjects into manageable steps
• 🚀 **Smart Recommendations** - I suggest optimal learning sequences

**Supported Learning Domains:**
• **AI Engineering** - Machine learning, deep learning, AI production
• **Web3 Development** - Blockchain, smart contracts, DeFi
• **Data Science** - Data analysis, statistics, machine learning

**How to get started:**
Just tell me what you'd like to learn! For example:
- "Teach me AI engineering"
- "I want to understand machine learning deeply"
- "Create a Web3 development path"
- "Explain deep learning concepts"

What would you like to explore? 🎓✨
            """)
            await ctx.send(sender, welcome_message)
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")
            
            user_input = item.text.lower()
            
            domain = None
            specific_concept = None
            
            if any(keyword in user_input for keyword in ["ai engineering", "ai engineer", "artificial intelligence"]):
                domain = "ai_engineering"
                if "machine learning" in user_input:
                    specific_concept = "machine learning"
                elif "deep learning" in user_input:
                    specific_concept = "deep learning"
                elif "neural network" in user_input:
                    specific_concept = "neural networks"
                    
            elif any(keyword in user_input for keyword in ["web3", "blockchain", "smart contract", "defi"]):
                domain = "web3_development"
                if "blockchain" in user_input:
                    specific_concept = "blockchain"
                elif "smart contract" in user_input:
                    specific_concept = "smart contracts"
                elif "cryptocurrency" in user_input:
                    specific_concept = "cryptocurrency"
                    
            elif any(keyword in user_input for keyword in ["data science", "data scientist", "data analysis"]):
                domain = "data_science"
                if "data analysis" in user_input:
                    specific_concept = "data analysis"
                elif "statistics" in user_input:
                    specific_concept = "statistics"
            
            if domain:
                response = await generate_enhanced_curriculum(domain, "beginner", specific_concept)
            elif "help" in user_input:
                response = """
**I'm your Enhanced Learning Agent powered by MeTTa Knowledge Graph!**

🧠 **My Special Capabilities:**
• **Concept Understanding** - I know how different topics relate to each other
• **Learning Dependencies** - I understand prerequisites and learning order
• **Personalized Paths** - I create curricula tailored to your needs
• **Deep Dives** - I can explain specific concepts in detail

🎯 **What I can help you with:**
• Create structured learning curricula
• Explain complex concepts and their relationships
• Suggest optimal learning sequences
• Connect you with relevant learning materials
• Track your learning progress

**Try asking me:**
- "Teach me AI engineering"
- "Explain machine learning concepts"
- "Create a Web3 development path"
- "What are the prerequisites for deep learning?"

What would you like to learn about? 🚀
                """
            else:
                response = f"""
I understand you want to learn about: "{item.text}"

I can help you with structured learning paths for:
• **AI Engineering** - Machine learning, deep learning, AI production systems
• **Web3 Development** - Blockchain, smart contracts, DeFi protocols
• **Data Science** - Data analysis, statistics, machine learning

My MeTTa Knowledge Graph integration helps me:
• Understand concept relationships and dependencies
• Create personalized learning sequences
• Explain how different topics connect
• Suggest optimal learning paths

Please specify which domain interests you, or ask me "help" to see all my capabilities! 🎓
                """
            
            response_message = create_text_chat(response)
            await ctx.send(sender, response_message)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_message = create_text_chat("""
👋 **Thank you for learning with me!**

🧠 **Remember:**
• Learning is a journey of connected concepts
• Understanding relationships between topics is key
• Take time to explore prerequisites and dependencies
• Connect with our Learning Materials Agent for resources

Keep exploring and building your knowledge! 🎓✨
            """)
            await ctx.send(sender, goodbye_message)
            
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

enhanced_agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    fund_agent_if_low(enhanced_agent.wallet.address())
    
    print(f"Enhanced Learning Agent address: {enhanced_agent.address}")
    print(f"Enhanced Learning Agent name: {enhanced_agent.name}")
    print("Starting Enhanced Learning Agent with MeTTa integration...")
    
    enhanced_agent.run()