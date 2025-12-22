from flask import Blueprint, request, jsonify, g
from auth import jwt_required
from config import supabase
from services.job_runner import start_job, cancel_job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['POST'])
@jwt_required
def create_job():
    """Create and start a new job"""
    data = request.get_json()
    
    if not data or not data.get('repo_url'):
        return jsonify({'error': 'repo_url is required'}), 400
    
    repo_url = data['repo_url'].strip()
    branch = data.get('branch', 'main')
    
    # Fix common GitHub URL mistakes
    if '/tree/' in repo_url:
        # Extract branch from URL like https://github.com/user/repo/tree/branch-name
        parts = repo_url.split('/tree/')
        repo_url = parts[0]
        if len(parts) > 1 and not data.get('branch'):
            branch = parts[1].split('/')[0]
    
    if '/blob/' in repo_url:
        repo_url = repo_url.split('/blob/')[0]
    
    # Ensure .git suffix works
    if not repo_url.endswith('.git') and 'github.com' in repo_url:
        repo_url = repo_url.rstrip('/')
    
    # Create job in database
    result = supabase.table('jobs').insert({
        'user_id': g.user_id,
        'repo_url': repo_url,
        'branch': branch,
        'status': 'pending'
    }).execute()
    
    if not result.data:
        return jsonify({'error': 'Failed to create job'}), 500
    
    job = result.data[0]
    
    # Start job execution
    start_job(job['id'], repo_url, branch)
    
    return jsonify(job), 201

@jobs_bp.route('', methods=['GET'])
@jwt_required
def list_jobs():
    """List all jobs for current user"""
    result = supabase.table('jobs')\
        .select('*')\
        .eq('user_id', g.user_id)\
        .order('created_at', desc=True)\
        .execute()
    
    return jsonify(result.data), 200

@jobs_bp.route('/<job_id>', methods=['GET'])
@jwt_required
def get_job(job_id):
    """Get a specific job"""
    result = supabase.table('jobs')\
        .select('*')\
        .eq('id', job_id)\
        .eq('user_id', g.user_id)\
        .execute()
    
    if not result.data:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(result.data[0]), 200

@jobs_bp.route('/<job_id>', methods=['DELETE'])
@jwt_required
def delete_job(job_id):
    """Delete a job"""
    # First check ownership
    check = supabase.table('jobs')\
        .select('id')\
        .eq('id', job_id)\
        .eq('user_id', g.user_id)\
        .execute()
    
    if not check.data:
        return jsonify({'error': 'Job not found'}), 404
    
    # Delete job (logs will cascade)
    supabase.table('jobs').delete().eq('id', job_id).execute()
    
    return jsonify({'message': 'Job deleted'}), 200

@jobs_bp.route('/<job_id>/cancel', methods=['POST'])
@jwt_required
def cancel_job_route(job_id):
    """Cancel a running job"""
    # Check ownership
    check = supabase.table('jobs')\
        .select('id, status')\
        .eq('id', job_id)\
        .eq('user_id', g.user_id)\
        .execute()
    
    if not check.data:
        return jsonify({'error': 'Job not found'}), 404
    
    if check.data[0]['status'] != 'running':
        return jsonify({'error': 'Job is not running'}), 400
    
    cancelled = cancel_job(job_id)
    
    if cancelled:
        return jsonify({'message': 'Job cancelled'}), 200
    
    return jsonify({'error': 'Failed to cancel job'}), 500

@jobs_bp.route('/<job_id>/logs', methods=['GET'])
@jwt_required
def get_job_logs(job_id):
    """Get logs for a job"""
    # Check ownership
    check = supabase.table('jobs')\
        .select('id')\
        .eq('id', job_id)\
        .eq('user_id', g.user_id)\
        .execute()
    
    if not check.data:
        return jsonify({'error': 'Job not found'}), 404
    
    result = supabase.table('job_logs')\
        .select('*')\
        .eq('job_id', job_id)\
        .order('created_at', desc=False)\
        .execute()
    
    return jsonify(result.data), 200

@jobs_bp.route('/<job_id>/retry', methods=['POST'])
@jwt_required
def retry_job(job_id):
    """Retry a failed job"""
    # Get original job
    result = supabase.table('jobs')\
        .select('*')\
        .eq('id', job_id)\
        .eq('user_id', g.user_id)\
        .execute()
    
    if not result.data:
        return jsonify({'error': 'Job not found'}), 404
    
    original = result.data[0]
    
    if original['status'] not in ['failed', 'cancelled']:
        return jsonify({'error': 'Can only retry failed or cancelled jobs'}), 400
    
    # Create new job
    new_job = supabase.table('jobs').insert({
        'user_id': g.user_id,
        'repo_url': original['repo_url'],
        'branch': original['branch'],
        'status': 'pending'
    }).execute()
    
    if not new_job.data:
        return jsonify({'error': 'Failed to create retry job'}), 500
    
    job = new_job.data[0]
    start_job(job['id'], original['repo_url'], original['branch'])
    
    return jsonify(job), 201
