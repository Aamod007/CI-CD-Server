import os
import shutil
from git import Repo

def clone_repo(repo_url, branch, target_dir):
    """Clone a git repository to target directory"""
    os.makedirs(target_dir, exist_ok=True)
    
    repo = Repo.clone_from(
        repo_url, 
        target_dir, 
        branch=branch, 
        depth=1,
        single_branch=True
    )
    return repo

def get_repo_info(repo_path):
    """Get latest commit info from cloned repo"""
    repo = Repo(repo_path)
    commit = repo.head.commit
    
    return {
        'commit': commit.hexsha[:7],
        'message': commit.message.strip(),
        'author': commit.author.name,
        'date': commit.committed_datetime.isoformat()
    }

def cleanup_workspace(workspace_dir):
    """Remove workspace directory"""
    try:
        if os.path.exists(workspace_dir):
            shutil.rmtree(workspace_dir)
    except Exception as e:
        print(f"Failed to cleanup workspace: {e}")
