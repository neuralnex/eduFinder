from uagents import Model

class Request(Model):
    message: str
    query_type: str = "general"
    domain: str = "ai_engineering"
    topic: str = ""

class Response(Model):
    message: str
    agent_type: str
    success: bool = True
    error: str = ""

class CurriculumRequest(Model):
    domain: str
    user_query: str

class CurriculumResponse(Model):
    curriculum: str
    success: bool = True
    error: str = ""

class MaterialsRequest(Model):
    topic: str
    domain: str
    include_youtube: bool = True

class MaterialsResponse(Model):
    materials: str
    youtube_videos: str = ""
    success: bool = True
    error: str = ""

class InsightsRequest(Model):
    concept: str
    domain: str
    query_type: str = "explain"

class InsightsResponse(Model):
    insights: str
    success: bool = True
    error: str = ""
