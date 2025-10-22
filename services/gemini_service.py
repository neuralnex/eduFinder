import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from services.user_context import user_context_manager

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

from config import GEMINI_API_KEY, YOUTUBE_API_KEY

try:
    from .metta_integration import MeTTaKnowledgeGraph
    METTA_AVAILABLE = True
except ImportError:
    METTA_AVAILABLE = False

load_dotenv()

class GeminiLearningService:
    def __init__(self):
        self.gemini_available = GEMINI_AVAILABLE and GEMINI_API_KEY
        self.youtube_available = YOUTUBE_AVAILABLE and YOUTUBE_API_KEY
        
        if self.gemini_available:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            self.client = None

    def _extract_concepts_from_query(self, query: str) -> List[str]:
        query_lower = query.lower()
        concepts = []
        
        words = query_lower.split()
        
        for i in range(len(words) - 1):
            two_word = f"{words[i]}_{words[i+1]}"
            if len(two_word) > 6:
                concepts.append(two_word)
        
        for word in words:
            if len(word) > 3 and word not in ["the", "and", "for", "with", "from", "that", "this", "will", "learn", "teach", "help", "want", "need"]:
                concepts.append(word)
        
        if not concepts:
            concepts = [query_lower.replace(" ", "_")]
        
        return concepts[:5]

    async def generate_curriculum(self, domain: str, user_query: str = "", user_id: str = None) -> str:
        if not self.gemini_available:
            return self._get_fallback_curriculum(domain)
        
        if domain in ["general", "general_tech", ""]:
            try:
                from .metta_integration import DynamicMeTTaKnowledgeGraph
                async with DynamicMeTTaKnowledgeGraph() as metta:
                    domain = await metta.detect_domain_from_query(user_query)
            except Exception as e:
                print(f"Dynamic domain detection error: {e}")
        
        metta_insights = ""
        if METTA_AVAILABLE:
            try:
                from .metta_integration import DynamicMeTTaKnowledgeGraph
                async with DynamicMeTTaKnowledgeGraph() as metta:
                    if metta.use_real_metta:
                        concepts = self._extract_concepts_from_query(user_query)
                        for concept in concepts[:3]:
                            metta_data = await metta.query_learning_concepts(domain, concept)
                            if metta_data and "Dynamic MeTTa Knowledge Graph" in metta_data.get("source", ""):
                                metta_insights += f"\n**Dynamic MeTTa Knowledge Graph Insights for {concept.replace('_', ' ').title()}:**\n"
                                if metta_data.get("prerequisites"):
                                    metta_insights += f"- **Prerequisites**: {', '.join(metta_data['prerequisites'])}\n"
                                if metta_data.get("related_concepts"):
                                    metta_insights += f"- **Related Concepts**: {', '.join(metta_data['related_concepts'])}\n"
                                if metta_data.get("learning_path"):
                                    metta_insights += f"- **Learning Path**: {' → '.join(metta_data['learning_path'])}\n"
                                if metta_data.get("difficulty_level"):
                                    metta_insights += f"- **Difficulty Level**: {metta_data['difficulty_level']}\n"
                                if metta_data.get("estimated_time"):
                                    metta_insights += f"- **Estimated Time**: {metta_data['estimated_time']}\n"
                                metta_insights += "\n"
            except Exception as e:
                print(f"Dynamic MeTTa integration error in curriculum generation: {e}")
                pass
        
        try:
            user_context_info = ""
            if user_id:
                user_context = user_context_manager.get_context(user_id)
                learning_level = "beginner" if user_context.learning_level.beginner else "intermediate" if user_context.learning_level.intermediate else "advanced" if user_context.learning_level.advanced else "beginner"
                learning_pace = user_context.preferences.pace
                preferred_duration = user_context.preferences.preferred_duration
                practice_focus = user_context.preferences.practice_focus
                daily_time = user_context.preferences.daily_time_commitment
                
                user_context_info = f"""
**User Learning Profile:**
- Learning Level: {learning_level}
- Learning Pace: {learning_pace}
- Preferred Duration: {preferred_duration}
- Daily Time Commitment: {daily_time}
- Practice Focus: {'Yes - emphasize hands-on projects' if practice_focus else 'No - focus on theory and concepts'}
- Current Topic: {user_context.current_topic or 'Not specified'}
- Learning Goals: {', '.join(user_context.learning_goals) if user_context.learning_goals else 'Not specified'}
"""
            
            prompt = f"""
            User Query: "{user_query}"
            Detected Domain: {domain}
            {user_context_info}
            
            Based on the user's specific query and learning profile, create a comprehensive educational plan that directly addresses what they want to learn.
            
            {metta_insights}
            
            **IMPORTANT**: Focus heavily on PRACTICE and HANDS-ON PROJECTS. Learning by doing is the most effective way to master any skill.
            
            Analyze the user's request and create a personalized learning path that includes:
            
            
            Brief introduction tailored to the user's specific request and what they will achieve
            
            
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
            
            What learners need to know before starting (tailored to their query)
            
            Total duration and recommended study schedule
            
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
    
    async def generate_conversational_response(self, user_query: str, context_type: str, user_id: str = None, topic: str = None, domain: str = None) -> str:
        if not self.gemini_available:
            return "I'm here to help you learn! What would you like to learn about?"
        
        try:
            user_context_info = ""
            if user_id:
                user_context = user_context_manager.get_context(user_id)
                learning_level = "beginner" if user_context.learning_level.beginner else "intermediate" if user_context.learning_level.intermediate else "advanced" if user_context.learning_level.advanced else "beginner"
                learning_pace = user_context.preferences.pace
                preferred_duration = user_context.preferences.preferred_duration
                practice_focus = user_context.preferences.practice_focus
                daily_time = user_context.preferences.daily_time_commitment
                
                user_context_info = f"""
**User Profile:**
- Learning Level: {learning_level}
- Learning Pace: {learning_pace}
- Preferred Duration: {preferred_duration}
- Daily Time: {daily_time}
- Practice Focus: {'Yes' if practice_focus else 'No'}
- Current Topic: {user_context.current_topic or 'None'}
- Learning Goals: {', '.join(user_context.learning_goals) if user_context.learning_goals else 'None'}
- Session Count: {user_context.session_count}
"""
            
            context_prompts = {
                "greeting": f"""
You are EduFinder, an intelligent learning companion. The user just greeted you: "{user_query}"

{user_context_info}

Respond naturally and warmly as a learning assistant. Be conversational, encouraging, and show enthusiasm for helping them learn. Ask what they'd like to learn about today. Keep it friendly and personal.
""",
                "gratitude": f"""
The user expressed gratitude: "{user_query}"

{user_context_info}

Respond warmly and encouragingly. Acknowledge their thanks and motivate them to continue learning. Ask what they'd like to learn next or if they need help with anything specific.
""",
                "learning_pace": f"""
The user mentioned their learning speed or pace: "{user_query}"

{user_context_info}

Respond with empathy and encouragement. Acknowledge that everyone learns differently and reassure them. Offer to create a learning plan that matches their pace. Be supportive and understanding.
""",
                "learning_request": f"""
The user wants to learn something: "{user_query}"

{user_context_info}

Topic: {topic or 'Not specified'}
Domain: {domain or 'Not specified'}

Respond enthusiastically about their learning goal. Show that you understand what they want to learn and their preferences. Be encouraging and mention that you'll create a personalized plan. Keep it conversational and motivating.
""",
                "general": f"""
The user said: "{user_query}"

{user_context_info}

Respond naturally as a helpful learning assistant. If you're not sure what they want, ask clarifying questions about their learning goals. Be friendly, encouraging, and guide them toward learning opportunities.
""",
                "curriculum_greeting": f"""
You are the Curriculum Agent, specialized in creating learning paths. The user greeted you: "{user_query}"

{user_context_info}

Respond as a curriculum specialist. Be enthusiastic about creating personalized learning plans. Mention your expertise in breaking down complex topics into manageable steps. Ask what they'd like to learn about.
""",
                "materials_greeting": f"""
You are the Materials Agent, specialized in finding educational resources. The user greeted you: "{user_query}"

{user_context_info}

Respond as a resource discovery specialist. Be enthusiastic about finding the best learning materials. Mention your ability to find videos, courses, books, and hands-on projects. Ask what resources they need.
""",
                "enhanced_greeting": f"""
You are the Enhanced Learning Agent, specialized in deep insights and concept analysis. The user greeted you: "{user_query}"

{user_context_info}

Respond as an insights specialist. Be enthusiastic about providing deep understanding and concept relationships. Mention your ability to explain complex topics and show connections between ideas. Ask what they'd like to understand deeply.
"""
            }
            
            prompt = context_prompts.get(context_type, context_prompts["general"])
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I'm here to help you learn! What would you like to learn about? (Error: {str(e)})"

    async def generate_learning_materials(self, topic: str, domain: str, user_query: str = "") -> str:
        if not self.gemini_available:
            return self._get_fallback_materials(topic, domain)

        if domain in ["general", "general_tech", ""]:
            try:
                from .metta_integration import DynamicMeTTaKnowledgeGraph
                async with DynamicMeTTaKnowledgeGraph() as metta:
                    domain = await metta.detect_domain_from_query(user_query)
            except Exception as e:
                print(f"Dynamic domain detection error: {e}")

        metta_insights = ""
        if METTA_AVAILABLE:
            try:
                from .metta_integration import DynamicMeTTaKnowledgeGraph
                async with DynamicMeTTaKnowledgeGraph() as metta:
                    if metta.use_real_metta:
                        metta_data = await metta.query_learning_concepts(domain, topic)
                        if metta_data and "Dynamic MeTTa Knowledge Graph" in metta_data.get("source", ""):
                            metta_insights += f"\n**Dynamic MeTTa Insights for {topic.replace('_', ' ').title()}:**\n"
                            if metta_data.get("prerequisites"):
                                metta_insights += f"- **Prerequisites**: {', '.join(metta_data['prerequisites'])}\n"
                            if metta_data.get("difficulty_level"):
                                metta_insights += f"- **Difficulty Level**: {metta_data['difficulty_level']}\n"
                            if metta_data.get("estimated_time"):
                                metta_insights += f"- **Estimated Time**: {metta_data['estimated_time']}\n"
                            metta_insights += "\n"
            except Exception as e:
                print(f"Dynamic MeTTa integration error in materials generation: {e}")

        try:
            prompt = f"""
            User Query: "{user_query}"
            Topic: {topic}
            Detected Domain: {domain}
            
            {metta_insights}
            
            Based on the user's specific request, provide targeted learning resources that directly address what they're looking for.
            
            Analyze their query and provide:
            
            **Learning Resources for {topic} in {domain.replace('_', ' ').title()}**
            
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
        
        if domain in ["general", "general_tech", ""]:
            try:
                from .metta_integration import DynamicMeTTaKnowledgeGraph
                async with DynamicMeTTaKnowledgeGraph() as metta:
                    domain = await metta.detect_domain_from_query(user_query)
            except Exception as e:
                print(f"Dynamic domain detection error: {e}")
        
        metta_insights = ""
        if METTA_AVAILABLE:
            try:
                from .metta_integration import DynamicMeTTaKnowledgeGraph
                async with DynamicMeTTaKnowledgeGraph() as metta:
                    if metta.use_real_metta:
                        metta_data = await metta.query_learning_concepts(domain, concept)
                        if metta_data and "Dynamic MeTTa Knowledge Graph" in metta_data.get("source", ""):
                            metta_insights += f"\n**Dynamic MeTTa Knowledge Graph Analysis for {concept.replace('_', ' ').title()}:**\n"
                            if metta_data.get("prerequisites"):
                                metta_insights += f"- **Prerequisites**: {', '.join(metta_data['prerequisites'])}\n"
                            if metta_data.get("related_concepts"):
                                metta_insights += f"- **Related Concepts**: {', '.join(metta_data['related_concepts'])}\n"
                            if metta_data.get("learning_path"):
                                metta_insights += f"- **Learning Sequence**: {' → '.join(metta_data['learning_path'])}\n"
                            if metta_data.get("difficulty_level"):
                                metta_insights += f"- **Difficulty Level**: {metta_data['difficulty_level']}\n"
                            if metta_data.get("estimated_time"):
                                metta_insights += f"- **Estimated Learning Time**: {metta_data['estimated_time']}\n"
                            if metta_data.get("definition"):
                                metta_insights += f"- **Definition**: {metta_data['definition']}\n"
                            metta_insights += "\n"
            except Exception as e:
                print(f"Dynamic MeTTa integration error in deep insights generation: {e}")
                pass
        
        try:
            prompt = f"""
            User Query: "{user_query}"
            Concept: {concept}
            Detected Domain: {domain}
            
            {metta_insights}
            
            Based on the user's specific question, provide deep insights that directly address what they want to understand.
            
            Analyze their query and provide:
            
            **Deep Insights: {concept} in {domain.replace('_', ' ').title()}**
            
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
        import os
        current_key = os.getenv('YOUTUBE_API_KEY')
        
        if not self.youtube_available or not current_key or current_key == 'invalid_key':
            print("[YOUTUBE API] Not available - returning empty list")
            return []
        
        try:
            youtube = build('youtube', 'v3', developerKey=current_key)
            
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=limit,
                type='video',
                order='relevance',
                videoDuration='medium',
                videoDefinition='high'
            ).execute()
            
            video_list = []
            video_ids = []
            
            for search_result in search_response.get('items', []):
                video_ids.append(search_result['id']['videoId'])
            
            if video_ids:
                video_response = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(video_ids)
                ).execute()
                
                for video in video_response.get('items', []):
                    snippet = video['snippet']
                    statistics = video['statistics']
                    content_details = video['contentDetails']
                    
                    video_list.append({
                        "title": snippet.get('title', 'Unknown Title'),
                        "channel": snippet.get('channelTitle', 'Unknown Channel'),
                        "duration": content_details.get('duration', 'Unknown Duration'),
                        "views": f"{int(statistics.get('viewCount', 0)):,} views",
                        "url": f"https://www.youtube.com/watch?v={video['id']}",
                        "embed_url": f"https://www.youtube.com/embed/{video['id']}",
                        "thumbnail": snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                        "description": snippet.get('description', '')[:100] + '...' if snippet.get('description') else '',
                        "published": snippet.get('publishedAt', 'Unknown Date')[:10]
                    })
            
            print(f"[YOUTUBE API] Found {len(video_list)} videos for query: {query}")
            return video_list
            
        except HttpError as e:
            print(f"[YOUTUBE API] HTTP Error: {e}")
            if e.resp.status == 403:
                print("[YOUTUBE API] Quota exceeded or API disabled")
            elif e.resp.status == 400:
                print("[YOUTUBE API] Invalid request parameters")
            return []
        except Exception as e:
            print(f"[YOUTUBE API] Unexpected error: {e}")
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
• **Documentation**: Python Docs (docs.python.org), MDN Web Docs (developer.mozilla.org)
• **Tutorials**: W3Schools (w3schools.com), TutorialsPoint (tutorialspoint.com)
• **Practice**: LeetCode (leetcode.com), HackerRank (hackerrank.com), Codewars (codewars.com)
• **Courses**: Coursera (coursera.org), edX (edx.org), Udemy (udemy.com)
• **Interactive Learning**: Codecademy (codecademy.com), freeCodeCamp (freecodecamp.org)

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
