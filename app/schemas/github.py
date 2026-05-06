from pydantic import BaseModel


class RepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: str
    description: str | None = None


class PullRequestResponse(BaseModel):
    number: int
    title: str
    state: str
    created_at: str
    author: str
    url: str


class GetPRRequest(BaseModel):
    owner:str
    repo:str

class FetchPR(BaseModel):
    owner:str
    repo:str
    pr_number:int