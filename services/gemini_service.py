import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from youtubesearchpython import VideosSearch
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

from config import GEMINI_API_KEY, YOUTUBE_API_KEY

load_dotenv()

class GeminiLearningService:
    def __init__(self):
        self.gemini_available = GEMINI_AVAILABLE and GEMINI_API_KEY
        self.youtube_available = YOUTUBE_AVAILABLE and YOUTUBE_API_KEY
        
        if self.gemini_available:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            self.client = None

    async def generate_curriculum(self, domain: str) -> str:
        if not self.gemini_available:
            return self._get_fallback_curriculum(domain)
        
        try:
            prompt = f"""
            Create a comprehensive learning curriculum for {domain}. 
            Include:
            1. Overview and prerequisites
            2. Learning modules with topics and duration
            3. Difficulty levels
            4. Estimated completion time
            5. Next steps for learners
            
            Format as a structured learning path with clear progression.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini curriculum generation failed: {e}")
            return self._get_fallback_curriculum(domain)

    async def generate_learning_materials(self, topic: str, domain: str) -> str:
        if not self.gemini_available:
            return self._get_fallback_materials(topic, domain)
        
        try:
            prompt = f"""
            For learning {topic} in {domain}, provide:
            1. Recommended learning resources
            2. Key concepts to focus on
            3. Practical projects to try
            4. Study tips and best practices
            5. Common pitfalls to avoid
            
            Make it actionable and beginner-friendly.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini materials generation failed: {e}")
            return self._get_fallback_materials(topic, domain)

    async def generate_deep_insights(self, concept: str, domain: str) -> str:
        if not self.gemini_available:
            return self._get_fallback_insights(concept, domain)
        
        try:
            prompt = f"""
            Provide deep insights about {concept} in {domain}:
            1. Core concepts and definitions
            2. Prerequisites and dependencies
            3. Related concepts and connections
            4. Learning progression and order
            5. Real-world applications
            6. Advanced topics to explore next
            
            Make it comprehensive and educational.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini insights generation failed: {e}")
            return self._get_fallback_insights(concept, domain)

    async def search_youtube_videos(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not self.youtube_available:
            return []
        
        try:
            videosSearch = VideosSearch(query, limit=limit)
            results = videosSearch.result()
            
            video_list = []
            for video in results.get('result', []):
                video_list.append({
                    "title": video.get('title'),
                    "channel": video.get('channel', {}).get('name'),
                    "duration": video.get('duration'),
                    "views": video.get('viewCount', {}).get('text'),
                    "url": video.get('link')
                })
            return video_list
        except Exception as e:
            print(f"YouTube search error: {e}")
            return []

    def _get_fallback_curriculum(self, domain: str) -> str:
        fallback_curricula = {
            "ai_engineering": """
**AI Engineering Learning Path**

**Overview**: Complete path to becoming an AI Engineer
**Duration**: 6-12 months
**Prerequisites**: Basic programming, Mathematics fundamentals

**Learning Modules:**

**Module 1: Foundations of AI**
• Duration: 4-6 weeks
• Difficulty: Beginner
• Topics: Machine Learning basics, Statistics, Linear Algebra

**Module 2: Deep Learning Fundamentals**
• Duration: 6-8 weeks
• Difficulty: Intermediate
• Topics: Neural Networks, CNN, RNN, Transformers

**Module 3: AI Engineering Practices**
• Duration: 8-10 weeks
• Difficulty: Advanced
• Topics: Model Deployment, MLOps, Production Systems

**Next Steps**: 
I can help you find specific resources and videos for each module!
            """,
            "web3_development": """
**Web3 Development Learning Path**

**Overview**: Complete path to becoming a Web3 Developer
**Duration**: 4-8 months
**Prerequisites**: JavaScript, Blockchain basics

**Learning Modules:**

**Module 1: Blockchain Fundamentals**
• Duration: 3-4 weeks
• Difficulty: Beginner
• Topics: Blockchain basics, Cryptography, Consensus mechanisms

**Module 2: Smart Contract Development**
• Duration: 6-8 weeks
• Difficulty: Intermediate
• Topics: Solidity, Ethereum, Smart contract patterns

**Module 3: DApp Development**
• Duration: 4-6 weeks
• Difficulty: Intermediate
• Topics: Web3.js, Frontend integration, Testing

**Next Steps**: 
I can help you find specific resources and videos for each module!
            """,
            "data_science": """
**Data Science Learning Path**

**Overview**: Complete path to becoming a Data Scientist
**Duration**: 6-10 months
**Prerequisites**: Python, Basic statistics

**Learning Modules:**

**Module 1: Data Analysis Fundamentals**
• Duration: 4-6 weeks
• Difficulty: Beginner
• Topics: Pandas, NumPy, Data visualization

**Module 2: Statistical Analysis**
• Duration: 6-8 weeks
• Difficulty: Intermediate
• Topics: Statistics, Hypothesis testing, A/B testing

**Module 3: Machine Learning**
• Duration: 8-10 weeks
• Difficulty: Intermediate
• Topics: Scikit-learn, Model evaluation, Feature engineering

**Next Steps**: 
I can help you find specific resources and videos for each module!
            """
        }
        return fallback_curricula.get(domain, "Sorry, I don't have a curriculum for that domain yet.")

    def _get_fallback_materials(self, topic: str, domain: str) -> str:
        return f"""
**Learning Resources for {topic} in {domain.title()}**

**Recommended Approach:**
1. Start with foundational concepts
2. Practice with hands-on projects
3. Join online communities
4. Build a portfolio

**Study Tips:**
• Break down complex topics into smaller parts
• Practice regularly to reinforce learning
• Apply concepts through real projects
• Don't hesitate to ask questions

**Next Steps**: 
I can help you find YouTube videos and additional resources!
        """

    def _get_fallback_insights(self, concept: str, domain: str) -> str:
        return f"""
**Deep Insights: {concept} in {domain.title()}**

**Core Concepts:**
• Understanding the fundamental principles
• Key terminology and definitions
• How it fits into the broader field

**Learning Path:**
1. Start with basics and fundamentals
2. Practice with examples and exercises
3. Explore advanced applications
4. Connect with related concepts

**Real-World Applications:**
• Industry use cases and examples
• Career opportunities and paths
• Future trends and developments

**Next Steps**: 
I can help you dive deeper into specific aspects!
        """

if __name__ == "__main__":
    async def test_gemini_service():
        print("Testing Gemini Learning Service")
        print("=" * 50)
        
        service = GeminiLearningService()
        print(f"Gemini Available: {service.gemini_available}")
        print(f"YouTube Available: {service.youtube_available}")
        
        # Test curriculum generation
        curriculum = await service.generate_curriculum("ai_engineering")
        print("\n--- AI Engineering Curriculum ---")
        print(curriculum)
        
        # Test YouTube search
        videos = await service.search_youtube_videos("machine learning tutorial", 3)
        print("\n--- YouTube Videos ---")
        for video in videos:
            print(f"• {video['title']} - {video['channel']}")

    import asyncio
    asyncio.run(test_gemini_service())
