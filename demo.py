#!/usr/bin/env python3

import asyncio
from agents.metta_integration import MeTTaKnowledgeGraph

async def demo_curriculum_creation():
    print("🎓 Learning Agents Demo")
    print("=" * 50)
    
    print("\n📚 Demo: Curriculum Creation")
    print("-" * 30)
    
    domains = ["ai_engineering", "web3_development", "data_science"]
    
    for domain in domains:
        print(f"\n🎯 Creating curriculum for: {domain.replace('_', ' ').title()}")
        
        async with MeTTaKnowledgeGraph() as metta:
            foundational_concepts = {
                "ai_engineering": ["machine learning", "deep learning"],
                "web3_development": ["blockchain", "smart contracts"],
                "data_science": ["data analysis", "statistics"]
            }
            
            concepts = foundational_concepts.get(domain, [])
            
            if concepts:
                learning_order = await metta.suggest_learning_order(domain, concepts)
                
                print(f"📋 Recommended Learning Sequence:")
                for i, concept in enumerate(learning_order, 1):
                    concept_data = await metta.query_learning_concepts(domain, concept)
                    definition = concept_data.get('definition', 'Learn about this important concept')
                    difficulty = concept_data.get('difficulty_level', 'Not specified')
                    time_estimate = concept_data.get('estimated_time', 'Not specified')
                    
                    print(f"  {i}. {concept.replace('_', ' ').title()}")
                    print(f"     📖 {definition}")
                    print(f"     🎯 Difficulty: {difficulty}")
                    print(f"     ⏱️ Time: {time_estimate}")

async def demo_resource_discovery():
    print("\n🎥 Demo: Resource Discovery")
    print("-" * 30)
    
    try:
        from youtubesearchpython import VideosSearch
        
        topics = [
            "machine learning tutorial",
            "blockchain explained", 
            "data science python"
        ]
        
        for topic in topics:
            print(f"\n🔍 Searching for: {topic}")
            
            videosSearch = VideosSearch(topic, limit=2)
            results = videosSearch.result()
            
            if results.get('result'):
                print("📺 Found videos:")
                for i, video in enumerate(results['result'], 1):
                    title = video.get('title', 'No title')
                    channel = video.get('channel', {}).get('name', 'Unknown channel')
                    duration = video.get('duration', 'Unknown duration')
                    url = video.get('link', '')
                    
                    print(f"  {i}. {title}")
                    print(f"     📺 {channel} | ⏱️ {duration}")
                    print(f"     🔗 {url}")
            else:
                print("  No videos found")
                
    except ImportError:
        print("⚠️ YouTube search not available (youtube-search-python not installed)")
        print("   Install with: pip install youtube-search-python")

async def demo_knowledge_graph():
    print("\n🧠 Demo: Knowledge Graph Integration")
    print("-" * 30)
    
    async with MeTTaKnowledgeGraph() as metta:
        concept = "machine learning"
        domain = "ai_engineering"
        
        print(f"\n🔍 Deep dive into: {concept}")
        
        concept_data = await metta.query_learning_concepts(domain, concept)
        
        if concept_data:
            print(f"📖 Definition: {concept_data.get('definition', 'No definition')}")
            
            prerequisites = concept_data.get('prerequisites', [])
            if prerequisites:
                print(f"📋 Prerequisites:")
                for prereq in prerequisites:
                    print(f"  • {prereq}")
            
            related_concepts = concept_data.get('related_concepts', [])
            if related_concepts:
                print(f"🔗 Related Concepts:")
                for related in related_concepts:
                    print(f"  • {related}")
            
            learning_path = concept_data.get('learning_path', [])
            if learning_path:
                print(f"📚 Learning Path:")
                for i, step in enumerate(learning_path, 1):
                    print(f"  {i}. {step}")

async def demo_agent_communication():
    print("\n🤖 Demo: Agent Communication")
    print("-" * 30)
    
    print("📱 Simulating agent conversation...")
    
    user_requests = [
        "Teach me AI engineering",
        "Get me resources for machine learning",
        "Explain deep learning concepts"
    ]
    
    for request in user_requests:
        print(f"\n👤 User: {request}")
        
        if "ai engineering" in request.lower():
            print("🤖 Curriculum Agent: I'll create a comprehensive AI engineering curriculum for you!")
            print("   📚 Module 1: Foundations of AI (4-6 weeks)")
            print("   📚 Module 2: Deep Learning Fundamentals (6-8 weeks)")
            print("   📚 Module 3: AI Engineering Practices (8-10 weeks)")
            print("   📚 Module 4: Specialized Applications (6-8 weeks)")
            
        elif "resources" in request.lower():
            print("🎥 Materials Agent: I'll find the best learning resources for you!")
            print("   📺 Recommended YouTube videos")
            print("   🎓 Online courses")
            print("   📖 Books and tutorials")
            print("   🛠️ Hands-on projects")
            
        elif "explain" in request.lower():
            print("🧠 Enhanced Learning Agent: Let me explain using our knowledge graph!")
            print("   🧠 Concept definitions and relationships")
            print("   📋 Prerequisites and dependencies")
            print("   🔗 Related concepts to explore")
            print("   📚 Optimal learning sequence")

async def main():
    print("🚀 Starting Learning Agents Demo...")
    
    try:
        await demo_curriculum_creation()
        await demo_resource_discovery()
        await demo_knowledge_graph()
        await demo_agent_communication()
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("  ✅ Curriculum creation with structured learning paths")
        print("  ✅ Resource discovery with YouTube integration")
        print("  ✅ Knowledge graph integration with MeTTa")
        print("  ✅ Multi-agent communication and collaboration")
        print("  ✅ Personalized learning recommendations")
        
        print("\n🚀 Ready for deployment to Agentverse!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)