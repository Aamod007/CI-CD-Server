"""
CI Server Python Client Example
Usage: python client_example.py
"""
import requests

BASE_URL = "http://localhost:5000/api"

class CIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    # Auth
    def register(self, email, password):
        res = requests.post(f"{self.base_url}/auth/register", 
                           json={"email": email, "password": password})
        data = res.json()
        if "token" in data:
            self.token = data["token"]
        return data
    
    def login(self, email, password):
        res = requests.post(f"{self.base_url}/auth/login",
                           json={"email": email, "password": password})
        data = res.json()
        if "token" in data:
            self.token = data["token"]
        return data
    
    def me(self):
        res = requests.get(f"{self.base_url}/auth/me", headers=self._headers())
        return res.json()
    
    # Jobs
    def create_job(self, repo_url, branch="main"):
        res = requests.post(f"{self.base_url}/jobs",
                           json={"repo_url": repo_url, "branch": branch},
                           headers=self._headers())
        return res.json()
    
    def list_jobs(self):
        res = requests.get(f"{self.base_url}/jobs", headers=self._headers())
        return res.json()
    
    def get_job(self, job_id):
        res = requests.get(f"{self.base_url}/jobs/{job_id}", headers=self._headers())
        return res.json()
    
    def get_logs(self, job_id):
        res = requests.get(f"{self.base_url}/jobs/{job_id}/logs", headers=self._headers())
        return res.json()
    
    def cancel_job(self, job_id):
        res = requests.post(f"{self.base_url}/jobs/{job_id}/cancel", headers=self._headers())
        return res.json()
    
    def retry_job(self, job_id):
        res = requests.post(f"{self.base_url}/jobs/{job_id}/retry", headers=self._headers())
        return res.json()
    
    def delete_job(self, job_id):
        res = requests.delete(f"{self.base_url}/jobs/{job_id}", headers=self._headers())
        return res.json()


if __name__ == "__main__":
    client = CIClient()
    
    # Login or register
    print("=== Login ===")
    result = client.login("test@example.com", "password123")
    print(result)
    
    # Create a job
    print("\n=== Create Job ===")
    job = client.create_job("https://github.com/pallets/flask", branch="main")
    print(job)
    
    # List jobs
    print("\n=== List Jobs ===")
    jobs = client.list_jobs()
    for j in jobs:
        print(f"  {j['id'][:8]}... | {j['status']} | {j['repo_url']}")
    
    # Get logs
    if job.get("id"):
        print(f"\n=== Logs for {job['id'][:8]}... ===")
        import time
        time.sleep(3)  # Wait for some logs
        logs = client.get_logs(job["id"])
        for log in logs:
            print(f"  [{log['level']}] {log['message']}")
