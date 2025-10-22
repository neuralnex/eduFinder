import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import asyncio

@dataclass
class LearningLevel:
    beginner: bool = False
    intermediate: bool = False
    advanced: bool = False
    expert: bool = False

@dataclass
class LearningPreferences:
    learning_style: str = "visual"
    pace: str = "moderate"
    focus_areas: List[str] = None
    avoid_topics: List[str] = None
    preferred_duration: str = "flexible"
    practice_focus: bool = True
    daily_time_commitment: str = "not specified"
    
    def __post_init__(self):
        if self.focus_areas is None:
            self.focus_areas = []
        if self.avoid_topics is None:
            self.avoid_topics = []

@dataclass
class UserContext:
    user_id: str
    name: Optional[str] = None
    learning_level: LearningLevel = None
    preferences: LearningPreferences = None
    conversation_history: List[Dict[str, Any]] = None
    current_topic: Optional[str] = None
    current_domain: Optional[str] = None
    learning_goals: List[str] = None
    strengths: List[str] = None
    weaknesses: List[str] = None
    last_interaction: Optional[datetime] = None
    session_count: int = 0
    
    def __post_init__(self):
        if self.learning_level is None:
            self.learning_level = LearningLevel()
        if self.preferences is None:
            self.preferences = LearningPreferences()
        if self.conversation_history is None:
            self.conversation_history = []
        if self.learning_goals is None:
            self.learning_goals = []
        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []

class UserContextManager:
    def __init__(self, storage_path: str = "user_contexts.json"):
        self.storage_path = storage_path
        self.contexts: Dict[str, UserContext] = {}
        self.load_contexts()
    
    def load_contexts(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for user_id, context_data in data.items():
                        context_data['learning_level'] = LearningLevel(**context_data.get('learning_level', {}))
                        context_data['preferences'] = LearningPreferences(**context_data.get('preferences', {}))
                        if context_data.get('last_interaction'):
                            context_data['last_interaction'] = datetime.fromisoformat(context_data['last_interaction'])
                        self.contexts[user_id] = UserContext(**context_data)
            except Exception as e:
                print(f"Error loading user contexts: {e}")
                self.contexts = {}
    
    def save_contexts(self):
        try:
            data = {}
            for user_id, context in self.contexts.items():
                context_dict = asdict(context)
                if context.last_interaction:
                    context_dict['last_interaction'] = context.last_interaction.isoformat()
                data[user_id] = context_dict
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving user contexts: {e}")
    
    def get_context(self, user_id: str) -> UserContext:
        if user_id not in self.contexts:
            self.contexts[user_id] = UserContext(user_id=user_id)
        return self.contexts[user_id]
    
    def update_context(self, user_id: str, **kwargs):
        context = self.get_context(user_id)
        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
        context.last_interaction = datetime.now()
        self.save_contexts()
    
    def add_conversation_entry(self, user_id: str, message: str, response: str, agent_type: str):
        context = self.get_context(user_id)
        context.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'response': response,
            'agent_type': agent_type
        })
        context.last_interaction = datetime.now()
        self.save_contexts()
    
    def assess_learning_level(self, user_id: str, message: str) -> str:
        context = self.get_context(user_id)
        
        beginner_indicators = [
            "beginner", "new to", "never learned", "don't know", "first time",
            "starting", "basics", "fundamentals", "intro", "introduction",
            "never done", "no experience", "complete beginner", "learning speed is not that good",
            "slow learner", "struggle", "difficult", "hard for me", "not good at"
        ]
        
        intermediate_indicators = [
            "some experience", "basic knowledge", "familiar with", "know basics",
            "intermediate", "somewhat", "a bit", "little bit", "some understanding",
            "have done some", "know a little", "basic level"
        ]
        
        advanced_indicators = [
            "advanced", "expert", "proficient", "experienced", "deep knowledge",
            "master", "professional", "expertise", "comprehensive", "thorough",
            "very good at", "excellent", "advanced level", "senior level"
        ]
        
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in beginner_indicators):
            context.learning_level.beginner = True
            return "beginner"
        elif any(indicator in message_lower for indicator in advanced_indicators):
            context.learning_level.advanced = True
            return "advanced"
        elif any(indicator in message_lower for indicator in intermediate_indicators):
            context.learning_level.intermediate = True
            return "intermediate"
        
        return "unknown"
    
    def extract_learning_goals(self, user_id: str, message: str) -> List[str]:
        context = self.get_context(user_id)
        
        goal_indicators = [
            "want to learn", "goal is", "trying to", "hoping to", "planning to",
            "need to", "should learn", "must learn", "aim to", "target"
        ]
        
        goals = []
        message_lower = message.lower()
        
        for indicator in goal_indicators:
            if indicator in message_lower:
                parts = message.split(indicator)
                if len(parts) > 1:
                    goal_text = parts[1].strip()
                    goals.append(goal_text)
        
        if goals:
            context.learning_goals.extend(goals)
            self.save_contexts()
        
        return goals
    
    def extract_learning_duration(self, user_id: str, message: str) -> str:
        context = self.get_context(user_id)
        
        duration_patterns = {
            "quick": ["quick", "fast", "rapid", "crash course", "intensive", "bootcamp"],
            "short": ["short", "brief", "few weeks", "month", "couple of weeks", "2-4 weeks"],
            "medium": ["few months", "3-6 months", "half year", "medium term"],
            "long": ["long term", "year", "extensive", "comprehensive", "thorough", "deep dive"],
            "flexible": ["flexible", "at my own pace", "whenever", "no rush", "take my time"]
        }
        
        message_lower = message.lower()
        
        for duration, patterns in duration_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                context.preferences.preferred_duration = duration
                self.save_contexts()
                return duration
        
        return context.preferences.preferred_duration
    
    def extract_practice_preferences(self, user_id: str, message: str) -> bool:
        context = self.get_context(user_id)
        
        practice_indicators = [
            "practice", "hands-on", "practical", "build", "create", "project",
            "exercise", "coding", "doing", "making", "implementing"
        ]
        
        theory_indicators = [
            "theory", "concepts", "understanding", "knowledge", "reading",
            "studying", "learning about", "explaining"
        ]
        
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in practice_indicators):
            context.preferences.practice_focus = True
            self.save_contexts()
            return True
        elif any(indicator in message_lower for indicator in theory_indicators):
            context.preferences.practice_focus = False
            self.save_contexts()
            return False
        
        return context.preferences.practice_focus
    
    def extract_time_commitment(self, user_id: str, message: str) -> str:
        context = self.get_context(user_id)
        
        time_patterns = {
            "30 minutes": ["30 min", "half hour", "30 minutes"],
            "1 hour": ["1 hour", "one hour", "60 min", "hour a day"],
            "2 hours": ["2 hours", "two hours", "couple hours"],
            "3+ hours": ["3 hours", "several hours", "many hours", "long sessions"],
            "flexible": ["flexible", "whenever", "spare time", "free time"]
        }
        
        message_lower = message.lower()
        
        for time_commitment, patterns in time_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                context.preferences.daily_time_commitment = time_commitment
                self.save_contexts()
                return time_commitment
        
        return context.preferences.daily_time_commitment
    
    def get_personalized_greeting(self, user_id: str) -> str:
        context = self.get_context(user_id)
        
        if context.session_count == 0:
            return f"Hello! I'm excited to be your learning companion. I'm here to help you learn anything you want, from programming to philosophy, cooking to quantum physics!"
        
        name_part = f", {context.name}" if context.name else ""
        level_part = ""
        
        if context.learning_level.beginner:
            level_part = " I remember you're just starting out - I'll make sure to explain everything clearly!"
        elif context.learning_level.intermediate:
            level_part = " I know you have some experience - I'll build on what you already know!"
        elif context.learning_level.advanced:
            level_part = " I see you're quite experienced - I'll dive deep into advanced concepts!"
        
        topic_part = ""
        if context.current_topic:
            topic_part = f" Are you continuing with {context.current_topic}?"
        
        return f"Welcome back{name_part}!{level_part}{topic_part} What would you like to learn today?"
    
    def get_adaptive_response_prefix(self, user_id: str, topic: str) -> str:
        context = self.get_context(user_id)
        
        if context.learning_level.beginner:
            return f"Great choice! Since you're new to {topic}, I'll start with the fundamentals and build up gradually. "
        elif context.learning_level.intermediate:
            return f"Perfect! I'll build on your existing knowledge of {topic} and help you advance further. "
        elif context.learning_level.advanced:
            return f"Excellent! I'll dive deep into advanced {topic} concepts and help you master the intricacies. "
        else:
            return f"Wonderful! I'll create a comprehensive learning experience for {topic} that adapts to your level. "
    
    def cleanup_old_contexts(self, days: int = 30):
        cutoff_date = datetime.now() - timedelta(days=days)
        to_remove = []
        
        for user_id, context in self.contexts.items():
            if context.last_interaction and context.last_interaction < cutoff_date:
                to_remove.append(user_id)
        
        for user_id in to_remove:
            del self.contexts[user_id]
        
        if to_remove:
            self.save_contexts()
            print(f"Cleaned up {len(to_remove)} old user contexts")

user_context_manager = UserContextManager()
