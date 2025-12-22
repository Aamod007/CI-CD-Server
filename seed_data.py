"""
Seed script to populate database with 50+ sample records
Run: python seed_data.py
"""
import random
from datetime import datetime, timedelta
from config import supabase
from auth import hash_password

# Sample data
REPOS = [
    "https://github.com/user/react-app",
    "https://github.com/user/flask-api",
    "https://github.com/user/node-server",
    "https://github.com/user/python-ml",
    "https://github.com/user/java-spring",
    "https://github.com/user/go-microservice",
    "https://github.com/user/rust-cli",
    "https://github.com/user/vue-dashboard",
    "https://github.com/user/django-blog",
    "https://github.com/user/express-api",
]

BRANCHES = ["main", "develop", "feature/auth", "feature/api", "hotfix/bug"]
STATUSES = ["success", "success", "success", "failed", "success", "cancelled", "success"]

def seed_users():
    """Create sample users"""
    users = []
    sample_users = [
        {"email": "admin@example.com", "password": "admin123"},
        {"email": "developer@example.com", "password": "dev123"},
        {"email": "tester@example.com", "password": "test123"},
        {"email": "demo@example.com", "password": "demo123"},
    ]
    
    for user_data in sample_users:
        # Check if user exists
        existing = supabase.table('users').select('id').eq('email', user_data['email']).execute()
        if existing.data:
            users.append(existing.data[0]['id'])
            print(f"User {user_data['email']} already exists")
            continue
            
        result = supabase.table('users').insert({
            'email': user_data['email'],
            'password_hash': hash_password(user_data['password'])
        }).execute()
        
        if result.data:
            users.append(result.data[0]['id'])
            print(f"Created user: {user_data['email']}")
    
    return users

def seed_jobs(user_ids, count=50):
    """Create sample jobs with varied timestamps"""
    jobs_created = 0
    
    for i in range(count):
        # Random timestamp within last 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        created_at = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
        
        status = random.choice(STATUSES)
        started_at = created_at + timedelta(seconds=random.randint(1, 10))
        
        # Set finished_at based on status
        if status in ['success', 'failed', 'cancelled']:
            duration = random.randint(10, 300)  # 10 seconds to 5 minutes
            finished_at = started_at + timedelta(seconds=duration)
        else:
            finished_at = None
        
        job_data = {
            'user_id': random.choice(user_ids),
            'repo_url': random.choice(REPOS),
            'branch': random.choice(BRANCHES),
            'status': status,
            'created_at': created_at.isoformat(),
            'started_at': started_at.isoformat(),
            'finished_at': finished_at.isoformat() if finished_at else None
        }
        
        result = supabase.table('jobs').insert(job_data).execute()
        
        if result.data:
            job_id = result.data[0]['id']
            jobs_created += 1
            
            # Add sample logs for each job
            seed_logs(job_id, status, job_data['repo_url'])
            
            if jobs_created % 10 == 0:
                print(f"Created {jobs_created} jobs...")
    
    return jobs_created

def seed_logs(job_id, status, repo_url):
    """Create sample logs for a job"""
    logs = [
        {'message': f'Starting job for {repo_url}', 'level': 'info'},
        {'message': 'Cloning repository...', 'level': 'info'},
        {'message': 'Cloned commit: abc1234 - Sample commit', 'level': 'info'},
        {'message': 'Found ci.json config', 'level': 'info'},
        {'message': 'Running: npm install', 'level': 'info'},
        {'message': 'Installing dependencies...', 'level': 'info'},
    ]
    
    if status == 'success':
        logs.extend([
            {'message': 'Running: npm test', 'level': 'info'},
            {'message': 'All tests passed', 'level': 'info'},
            {'message': 'Job completed successfully', 'level': 'info'},
        ])
    elif status == 'failed':
        logs.extend([
            {'message': 'Running: npm test', 'level': 'info'},
            {'message': 'Test failed: expected true but got false', 'level': 'error'},
            {'message': 'Job failed', 'level': 'error'},
        ])
    elif status == 'cancelled':
        logs.append({'message': 'Job cancelled by user', 'level': 'warn'})
    
    for log in logs:
        supabase.table('job_logs').insert({
            'job_id': job_id,
            'message': log['message'],
            'level': log['level']
        }).execute()

def main():
    print("=" * 50)
    print("Seeding database with sample data...")
    print("=" * 50)
    
    # Create users
    print("\n[1/2] Creating users...")
    user_ids = seed_users()
    
    if not user_ids:
        print("Error: No users created!")
        return
    
    # Create jobs
    print("\n[2/2] Creating jobs...")
    jobs_count = seed_jobs(user_ids, count=55)
    
    print("\n" + "=" * 50)
    print(f"Seeding complete!")
    print(f"  - Users: {len(user_ids)}")
    print(f"  - Jobs: {jobs_count}")
    print("=" * 50)
    print("\nSample login credentials:")
    print("  Email: demo@example.com")
    print("  Password: demo123")

if __name__ == "__main__":
    main()
