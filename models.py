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
    original_sender: str = ""
    request_id: str = ""

class CurriculumResponse(Model):
    curriculum: str
    success: bool = True
    error: str = ""
    request_id: str = ""

class MaterialsRequest(Model):
    topic: str
    domain: str
    user_query: str
    include_youtube: bool = True
    original_sender: str = ""
    request_id: str = ""

class MaterialsResponse(Model):
    materials: str
    youtube_videos: str = ""
    success: bool = True
    error: str = ""
    request_id: str = ""

class InsightsRequest(Model):
    concept: str
    domain: str
    query_type: str = "explain"
    user_query: str = ""
    original_sender: str = ""
    request_id: str = ""

class InsightsResponse(Model):
    insights: str
    success: bool = True
    error: str = ""
    request_id: str = ""
