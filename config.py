import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Load .env from the same directory as this file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
JWT_SECRET = os.getenv('JWT_SECRET', 'change-this-secret')
PORT = int(os.getenv('PORT', 5000))
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', './workspaces')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
