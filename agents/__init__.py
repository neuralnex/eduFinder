__version__ = "1.0.0"
__author__ = "ASI Alliance Hackathon Team"

from .curriculum_agent import agent as curriculum_agent
from .materials_agent import materials_agent
from .enhanced_curriculum_agent import enhanced_agent
from .metta_integration import MeTTaKnowledgeGraph

__all__ = [
    "curriculum_agent",
    "materials_agent", 
    "enhanced_agent",
    "MeTTaKnowledgeGraph"
]