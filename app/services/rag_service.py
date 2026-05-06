from langchain_text_splitters import RecursiveCharacterTextSplitter

def pr_chunks(files_data:list,github_id:int,repo_name:str,pr_number:int):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap = 100
    )

    documents = []

    for file in files_data:
        patch_text = file.get("patch")

        if not patch_text:
            continue
        filename = file.get("filename") 

       
        if filename.endswith((".gitignore", ".md", ".txt")):
            continue

        structured_text = f"""
        File: {filename}

        Code Changes:
        {patch_text}
        """

        chunks = splitter.split_text(structured_text)

        for chunk in chunks:
            documents.append({
                "content":chunk.strip(),
                "metadata": {
                    "github_user_id": github_id,
                    "repo_name": repo_name,
                    "pr_number": pr_number,
                    "file_name": filename
                }
            })

    return documents

