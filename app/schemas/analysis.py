from pydantic import BaseModel

class PRRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int
    query: str

class PRAnalysisResponse(BaseModel):
    analysis: str

class PRSummaryRequest(BaseModel):
    owner: str 
    repo: str 
    pr_number: int


class PRSummaryResponse(BaseModel):
    summary: str