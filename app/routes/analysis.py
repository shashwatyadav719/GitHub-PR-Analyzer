from fastapi import APIRouter, Depends,HTTPException
from app.utils.jwt_handler import get_current_user
from app.services.vector_db_service import query_embeddings
from app.services.llm_service import generate_pr_analysis,generate_pr_summary
from app.schemas.analysis import PRRequest,PRAnalysisResponse,PRSummaryRequest,PRSummaryResponse
from app.services.pr_service import process_pr_embeddings
from app.services.repo_context_service import get_repo_context

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/pr/chat",response_model=PRAnalysisResponse)
async def chat_pr(request: PRRequest, current_user: dict = Depends(get_current_user)):

    github_token = current_user["github_token"]
    github_user_id = current_user["github_user_id"]

    await process_pr_embeddings(
        github_token,
        github_user_id,
        request.owner,
        request.repo,
        request.pr_number
    )

    relevant_chunks = query_embeddings(
        query=request.query,
        github_id=github_user_id,
        repo_name=request.repo,
        pr_number=request.pr_number,
    )
    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant data found for this PR."
        )

    repo_context = await get_repo_context(
        github_token,
        request.owner,
        request.repo
    )

    analysis = generate_pr_analysis(
        query=request.query,
        context_chunks=relevant_chunks,
        repo_context=repo_context
    )

    return {"analysis": analysis}


@router.post("/pr/summary",response_model=PRSummaryResponse)
async def pr_summary(request: PRSummaryRequest, current_user: dict = Depends(get_current_user)):

    github_token = current_user["github_token"]
    github_user_id = current_user["github_user_id"]

    await process_pr_embeddings(
        github_token,
        github_user_id,
        request.owner,
        request.repo,
        request.pr_number
    )

    relevant_chunks = query_embeddings(
        query="Summarize this pull request",
        github_id=github_user_id,
        repo_name=request.repo,
        pr_number=request.pr_number,
    )

    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail="No data available to generate summary"
        )

    repo_context = await get_repo_context(
        github_token,
        request.owner,
        request.repo
    )

    summary = generate_pr_summary(
        context_chunks=relevant_chunks,
        repo_context=repo_context
    )

    return {"summary": summary}