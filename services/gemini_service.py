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

    async def generate_curriculum(self, domain: str, user_query: str = "") -> str:
        if not self.gemini_available:
            return self._get_fallback_curriculum(domain)
        
        try:
            prompt = f"""
            User Query: "{user_query}"
            Domain: {domain}
            
            Based on the user's specific query, create a comprehensive educational plan that directly addresses what they want to learn.
            
            Analyze the user's request and create a personalized learning path that includes:
            
            # {domain.replace('_', ' ').title()} Educational Plan
            
            ## Overview
            Brief introduction tailored to the user's specific request and what they will achieve
            
            ## Learning Path (Step-by-Step)
            
            ### Step 1: [Topic Name]
            **Duration**: [X weeks/hours]
            **Difficulty**: [Beginner/Intermediate/Advanced]
            **What you'll learn**: [Specific skills/concepts relevant to their query]
            
            **Learning Resources**:
            • **Course**: [Course name] - [Direct link]
            • **Documentation**: [Official docs] - [Link]
            • **Tutorial**: [Tutorial name] - [Link]
            • **Practice**: [Practice platform] - [Link]
            
            **YouTube Videos**:
            • [Video title] - [Channel] - [Link]
            • [Video title] - [Channel] - [Link]
            
            **Projects to Build**:
            • [Project name]: [Description] - [Tutorial link]
            
            [Continue for 5-8 steps covering the complete learning journey based on their specific request]
            
            ## Prerequisites
            What learners need to know before starting (tailored to their query)
            
            ## Estimated Timeline
            Total duration and recommended study schedule
            
            ## Next Steps
            How to continue learning after completing this plan
            
            Make it practical with real, working links and specific resources.
            Focus on hands-on learning with projects and practical applications.
            Tailor everything to directly address the user's specific learning request.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini curriculum generation failed: {e}")
            return self._get_fallback_curriculum(domain)

    async def generate_learning_materials(self, topic: str, domain: str, user_query: str = "") -> str:
        if not self.gemini_available:
            return self._get_fallback_materials(topic, domain)

        try:
            prompt = f"""
            User Query: "{user_query}"
            Topic: {topic}
            Domain: {domain}
            
            Based on the user's specific request, provide targeted learning resources that directly address what they're looking for.
            
            Analyze their query and provide:
            
            **Learning Resources for {topic} in {domain.title()}**
            
            **Essential Resources** (tailored to their specific request):
            • **Courses**: [Specific courses relevant to their query] - [Direct links]
            • **Documentation**: [Official docs] - [Links]
            • **Tutorials**: [Tutorials that match their needs] - [Links]
            • **Practice Platforms**: [Relevant practice sites] - [Links]
            
            **Recommended Approach** (based on their query):
            [Personalized learning approach based on what they specifically asked for]
            
            **Study Tips** (tailored to their request):
            [Specific tips relevant to their learning goals]
            
            **Next Steps** (based on their specific needs):
            [What they should do next based on their query]
            
            Make it actionable and directly address their specific learning request.
            Include actual working links and resources that match their query.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini materials generation failed: {e}")
            return self._get_fallback_materials(topic, domain)

    async def generate_deep_insights(self, concept: str, domain: str, user_query: str = "") -> str:
        if not self.gemini_available:
            return self._get_fallback_insights(concept, domain)
        
        try:
            prompt = f"""
            User Query: "{user_query}"
            Concept: {concept}
            Domain: {domain}
            
            Based on the user's specific question, provide deep insights that directly address what they want to understand.
            
            Analyze their query and provide:
            
            **Deep Insights: {concept} in {domain.title()}**
            
            **Core Understanding** (tailored to their specific question):
            [Explain the concept based on what they specifically asked about]
            
            **Key Relationships** (relevant to their query):
            [How this concept relates to other topics based on their specific interest]
            
            **Prerequisites** (based on their learning level):
            [What they need to know first, tailored to their question]
            
            **Practical Applications** (relevant to their query):
            [Real-world examples that match their specific interest]
            
            **Common Misconceptions** (related to their question):
            [Important clarifications based on their specific query]
            
            **Next Learning Steps** (based on their specific needs):
            [What to learn next based on their question]
            
            Make it directly relevant to their specific question and learning goals.
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
                    "title": video.get('title', 'Unknown Title'),
                    "channel": video.get('channel', {}).get('name', 'Unknown Channel'),
                    "duration": video.get('duration', 'Unknown Duration'),
                    "views": video.get('viewCount', {}).get('text', 'Unknown Views'),
                    "url": video.get('link', ''),
                    "description": video.get('descriptionSnippet', [{}])[0].get('text', '')[:100] + '...' if video.get('descriptionSnippet') else '',
                    "published": video.get('publishedTime', 'Unknown Date')
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

**Essential Links:**
• **Documentation**: https://docs.python.org/ (Python), https://developer.mozilla.org/ (Web)
• **Tutorials**: https://www.w3schools.com/, https://www.tutorialspoint.com/
• **Practice**: https://leetcode.com/, https://www.hackerrank.com/
• **Courses**: https://www.coursera.org/, https://www.edx.org/, https://www.udemy.com/

**Recommended Approach:**
1. Start with foundational concepts
2. Practice with hands-on projects
3. Join online communities (Reddit, Stack Overflow, Discord)
4. Build a portfolio on GitHub

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
        
        curriculum = await service.generate_curriculum("ai_engineering")
        print("\n--- AI Engineering Curriculum ---")
        print(curriculum)
        
        videos = await service.search_youtube_videos("machine learning tutorial", 3)
        print("\n--- YouTube Videos ---")
        for video in videos:
            print(f"• {video['title']} - {video['channel']}")

    import asyncio
    asyncio.run(test_gemini_service())
