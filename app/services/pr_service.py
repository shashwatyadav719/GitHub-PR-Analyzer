from app.services.github_service import get_pr_files
from app.services.rag_service import pr_chunks
from app.services.embedding_service import generate_embeddings
from app.services.vector_db_service import store_embeddings, check_pr_exists
from fastapi import HTTPException


async def process_pr_embeddings(github_token: str,github_user_id: int,owner: str,repo: str,pr_number: int):

    exists = check_pr_exists(
        github_user_id=github_user_id,
        repo_name=repo,
        pr_number=pr_number
    )

    if exists:
        return

    files = await get_pr_files(
        github_token=github_token,
        owner=owner,
        repo=repo,
        pr_number=pr_number
    )

    if not files:
        raise HTTPException(
            status_code=404,
            detail="No files found in this PR"
        )

    chunks = pr_chunks(
        files_data=files,
        github_id=github_user_id,
        repo_name=repo,
        pr_number=pr_number
    )

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No valid code changes to process"
        )

    embed_docs = generate_embeddings(chunks)

    if not embed_docs:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate embeddings"
        )

    store_embeddings(embed_docs)