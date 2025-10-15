import os
from dotenv import load_dotenv

load_dotenv()

AGENT_SEED = os.getenv("AGENT_SEED")
AGENT_NAME = "LearningPathAgent"
AGENT_DESCRIPTION = "An AI agent that creates personalized learning curricula and provides educational materials"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

METTA_ENDPOINT = os.getenv("METTA_ENDPOINT", "http://localhost:8080")
METTA_SPACE = os.getenv("METTA_SPACE", "learning_space")
METTA_USE_MOCK = os.getenv("METTA_USE_MOCK", "false").lower() == "true"

AGENTVERSE_ENDPOINT = os.getenv("AGENTVERSE_ENDPOINT", "https://agentverse.ai")