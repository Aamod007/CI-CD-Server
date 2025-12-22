import os
import json
import subprocess
import threading
from datetime import datetime
from config import supabase, WORKSPACE_DIR
from services.git_service import clone_repo, get_repo_info, cleanup_workspace

# Track running jobs
running_jobs = {}

def start_job(job_id, repo_url, branch):
    """Start job execution in background thread"""
    thread = threading.Thread(target=_run_job, args=(job_id, repo_url, branch))
    thread.start()
    running_jobs[job_id] = thread

def _run_job(job_id, repo_url, branch):
    """Execute the job pipeline"""
    workspace_dir = os.path.join(WORKSPACE_DIR, job_id)
    
    try:
        # Update status to running
        _update_job_status(job_id, 'running')
        _add_log(job_id, f'Starting job for {repo_url} (branch: {branch})', 'info')
        
        # Clone repository
        _add_log(job_id, 'Cloning repository...', 'info')
        clone_repo(repo_url, branch, workspace_dir)
        
        repo_info = get_repo_info(workspace_dir)
        _add_log(job_id, f"Cloned commit: {repo_info['commit']} - {repo_info['message']}", 'info')
        
        # Check for CI config or auto-detect project type
        ci_config_path = os.path.join(workspace_dir, 'ci.json')
        commands = None
        
        if os.path.exists(ci_config_path):
            try:
                with open(ci_config_path, 'r', encoding='utf-8') as f:
                    ci_config = json.load(f)
                    commands = ci_config.get('commands', [])
                _add_log(job_id, 'Found ci.json config', 'info')
            except Exception as e:
                _add_log(job_id, f'Error reading ci.json: {str(e)}', 'error')
                commands = _detect_project_commands(workspace_dir)
        else:
            # Auto-detect project type
            commands = _detect_project_commands(workspace_dir)
            _add_log(job_id, f'Auto-detected project type', 'info')
        
        if not commands:
            _add_log(job_id, 'No commands to run', 'warn')
            _update_job_status(job_id, 'success')
            return
        
        # Execute commands
        for cmd in commands:
            _add_log(job_id, f'Running: {cmd}', 'info')
            success = _execute_command(job_id, cmd, workspace_dir)
            
            if not success:
                _update_job_status(job_id, 'failed')
                _add_log(job_id, 'Job failed', 'error')
                cleanup_workspace(workspace_dir)
                return
        
        _update_job_status(job_id, 'success')
        _add_log(job_id, 'Job completed successfully', 'info')
        
    except Exception as e:
        _add_log(job_id, f'Error: {str(e)}', 'error')
        _update_job_status(job_id, 'failed')
    finally:
        cleanup_workspace(workspace_dir)
        running_jobs.pop(job_id, None)

def _execute_command(job_id, command, cwd):
    """Execute a shell command and stream logs"""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ, 'CI': 'true'}
        )
        
        for line in process.stdout:
            line = line.strip()
            if line:
                _add_log(job_id, line, 'info')
        
        process.wait()
        return process.returncode == 0
        
    except Exception as e:
        _add_log(job_id, f'Process error: {str(e)}', 'error')
        return False

def cancel_job(job_id):
    """Cancel a running job"""
    if job_id in running_jobs:
        # Note: Thread cancellation is limited in Python
        # For production, use a process-based approach
        running_jobs.pop(job_id, None)
        _update_job_status(job_id, 'cancelled')
        _add_log(job_id, 'Job cancelled by user', 'warn')
        return True
    return False

def _update_job_status(job_id, status):
    """Update job status in database"""
    updates = {'status': status}
    
    if status == 'running':
        updates['started_at'] = datetime.utcnow().isoformat()
    elif status in ['success', 'failed', 'cancelled']:
        updates['finished_at'] = datetime.utcnow().isoformat()
    
    supabase.table('jobs').update(updates).eq('id', job_id).execute()

def _add_log(job_id, message, level='info'):
    """Add log entry to database"""
    supabase.table('job_logs').insert({
        'job_id': job_id,
        'message': message,
        'level': level
    }).execute()


def _detect_project_commands(workspace_dir):
    """Auto-detect project type and return appropriate commands"""
    
    # Python project
    if os.path.exists(os.path.join(workspace_dir, 'requirements.txt')):
        cmds = ['pip install -r requirements.txt']
        if os.path.exists(os.path.join(workspace_dir, 'pytest.ini')) or \
           os.path.exists(os.path.join(workspace_dir, 'tests')):
            cmds.append('pytest')
        elif os.path.exists(os.path.join(workspace_dir, 'setup.py')):
            cmds.append('python setup.py test')
        return cmds
    
    # Python with pyproject.toml
    if os.path.exists(os.path.join(workspace_dir, 'pyproject.toml')):
        return ['pip install .', 'pytest']
    
    # Node.js project
    if os.path.exists(os.path.join(workspace_dir, 'package.json')):
        return ['npm install', 'npm test']
    
    # Go project
    if os.path.exists(os.path.join(workspace_dir, 'go.mod')):
        return ['go build ./...', 'go test ./...']
    
    # Rust project
    if os.path.exists(os.path.join(workspace_dir, 'Cargo.toml')):
        return ['cargo build', 'cargo test']
    
    # Java/Maven
    if os.path.exists(os.path.join(workspace_dir, 'pom.xml')):
        return ['mvn clean install']
    
    # Java/Gradle
    if os.path.exists(os.path.join(workspace_dir, 'build.gradle')):
        return ['./gradlew build']
    
    # Default: just list files
    return ['echo "No recognized project type. Add ci.json to configure."', 'dir' if os.name == 'nt' else 'ls -la']
