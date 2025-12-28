# 🚀 CI/CD Automation Server

A lightweight, self-hosted Continuous Integration/Continuous Deployment server built with Flask, JWT authentication, and Supabase. Execute automated pipelines for any Git repository with real-time log streaming.

🌐 **Live Demo:** [https://ci-cd-server-0lka.onrender.com](https://ci-cd-server-0lka.onrender.com)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Configuration](#configuration)
  - [Running the Server](#running-the-server)
- [Usage](#-usage)
  - [Web Interface](#web-interface)
  - [API Endpoints](#api-endpoints)
  - [Python Client](#python-client)
- [CI Configuration](#-ci-configuration)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🔐 JWT Authentication** - Secure user registration and login with raw JWT (no third-party auth)
- **📦 Git Integration** - Clone any public Git repository and execute pipelines
- **⚡ Real-time Logs** - Stream execution logs to the UI in real-time
- **🔄 Full CRUD Operations** - Create, Read, Update, Delete jobs via REST API
- **🎯 Auto-Detection** - Automatically detect project type (Python, Node.js, Java, Go, Rust)
- **📊 Job Management** - Track job status (pending, running, success, failed, cancelled)
- **🎨 Modern Web UI** - Dark-themed responsive interface for job management
- **🔁 Retry & Cancel** - Retry failed jobs or cancel running ones
- **☁️ Supabase Backend** - PostgreSQL database with real-time capabilities

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
├─────────────────────────────────────────────────────────────────┤
│   Web Browser (UI)          │        Python Client / cURL       │
└──────────────┬──────────────┴──────────────┬────────────────────┘
               │                             │
               ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask REST API                             │
├─────────────────────────────────────────────────────────────────┤
│  /api/auth/*  (Register, Login, Me)                             │
│  /api/jobs/*  (CRUD Operations)                                 │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Services                              │
├────────────────────────┬────────────────────────────────────────┤
│   Auth Service         │         Job Runner Service             │
│   - JWT Generation     │         - Git Clone                    │
│   - Password Hashing   │         - Command Execution            │
│   - Token Validation   │         - Log Streaming                │
└────────────────────────┴────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase (PostgreSQL)                        │
├─────────────────────────────────────────────────────────────────┤
│   users          │      jobs           │      job_logs          │
│   - id           │      - id           │      - id              │
│   - email        │      - user_id      │      - job_id          │
│   - password     │      - repo_url     │      - message         │
│   - created_at   │      - status       │      - level           │
└──────────────────┴──────────────────────┴───────────────────────┘
```

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+, Flask 3.0 |
| Authentication | PyJWT, bcrypt |
| Database | Supabase (PostgreSQL) |
| Git Operations | GitPython |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Process Management | Python subprocess, threading |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git installed and configured
- Supabase account (free tier works)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ci-server.git
   cd ci-server
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

1. **Create a Supabase project** at [supabase.com](https://supabase.com)

2. **Run the schema** in Supabase SQL Editor:
   ```sql
   -- Users table (for JWT auth)
   create table if not exists users (
     id uuid primary key default gen_random_uuid(),
     email text unique not null,
     password_hash text not null,
     created_at timestamptz default now()
   );

   -- Jobs table
   create table if not exists jobs (
     id uuid primary key default gen_random_uuid(),
     user_id uuid references users(id) on delete cascade,
     repo_url text not null,
     branch text default 'main',
     status text default 'pending',
     created_at timestamptz default now(),
     started_at timestamptz,
     finished_at timestamptz
   );

   -- Job logs table
   create table if not exists job_logs (
     id uuid primary key default gen_random_uuid(),
     job_id uuid references jobs(id) on delete cascade,
     message text,
     level text default 'info',
     created_at timestamptz default now()
   );

   -- Indexes
   create index if not exists idx_jobs_user_id on jobs(user_id);
   create index if not exists idx_jobs_status on jobs(status);
   create index if not exists idx_job_logs_job_id on job_logs(job_id);
   ```

### Configuration

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-service-role-key
   JWT_SECRET=your-super-secret-key-change-this
   PORT=5000
   WORKSPACE_DIR=./workspaces
   ```

   > ⚠️ **Important**: Use the **Service Role Key** from Supabase (not the anon key)

### Running the Server

```bash
python app.py
```

Server will start at `http://localhost:5000`

---

## 📖 Usage

### Web Interface

1. Open `http://localhost:5000` in your browser
2. Register a new account or login
3. Enter a Git repository URL and branch
4. Click "Run Job" to start the pipeline
5. Click "Logs" to view real-time execution

### API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login, get JWT token | No |
| GET | `/api/auth/me` | Get current user | Yes |
| POST | `/api/jobs` | Create new job | Yes |
| GET | `/api/jobs` | List all jobs | Yes |
| GET | `/api/jobs/<id>` | Get job details | Yes |
| GET | `/api/jobs/<id>/logs` | Get job logs | Yes |
| POST | `/api/jobs/<id>/cancel` | Cancel running job | Yes |
| POST | `/api/jobs/<id>/retry` | Retry failed job | Yes |
| DELETE | `/api/jobs/<id>` | Delete job | Yes |

### Python Client

```python
from client_example import CIClient

# Initialize client
client = CIClient()

# Register or login
client.register("user@example.com", "password123")
# or
client.login("user@example.com", "password123")

# Create a job
job = client.create_job("https://github.com/user/repo", branch="main")
print(f"Job ID: {job['id']}")

# Check job status
status = client.get_job(job['id'])
print(f"Status: {status['status']}")

# Get logs
logs = client.get_logs(job['id'])
for log in logs:
    print(f"[{log['level']}] {log['message']}")

# Other operations
client.list_jobs()
client.cancel_job(job['id'])
client.retry_job(job['id'])
client.delete_job(job['id'])
```

### cURL Examples

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Create job (replace TOKEN with your JWT)
curl -X POST http://localhost:5000/api/jobs \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"repo_url":"https://github.com/user/repo","branch":"main"}'
```

---

## ⚙️ CI Configuration

### Using ci.json

Add a `ci.json` file to your repository root:

```json
{
  "commands": [
    "pip install -r requirements.txt",
    "pytest -v",
    "echo Build completed!"
  ]
}
```

### Auto-Detection

If no `ci.json` is found, the server auto-detects project type:

| Project Type | Detection File | Default Commands |
|--------------|----------------|------------------|
| Python | `requirements.txt` | `pip install -r requirements.txt`, `pytest` |
| Python | `pyproject.toml` | `pip install .`, `pytest` |
| Node.js | `package.json` | `npm install`, `npm test` |
| Go | `go.mod` | `go build ./...`, `go test ./...` |
| Rust | `Cargo.toml` | `cargo build`, `cargo test` |
| Java (Maven) | `pom.xml` | `mvn clean install` |
| Java (Gradle) | `build.gradle` | `./gradlew build` |

### Example ci.json Files

**Python Project:**
```json
{
  "commands": [
    "pip install -r requirements.txt",
    "python -m pytest tests/ -v",
    "python main.py --check"
  ]
}
```

**Node.js Project:**
```json
{
  "commands": [
    "npm ci",
    "npm run lint",
    "npm test",
    "npm run build"
  ]
}
```

**Java Project:**
```json
{
  "commands": [
    "javac src/*.java -d out/",
    "java -cp out/ Main",
    "echo Compilation successful!"
  ]
}
```

---

## 📁 Project Structure

```
ci-server/
├── app.py                 # Flask application entry point
├── config.py              # Configuration and Supabase client
├── auth.py                # JWT authentication logic
├── requirements.txt       # Python dependencies
├── schema.sql             # Database schema
├── .env.example           # Environment template
├── .gitignore
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py     # /api/auth/* endpoints
│   └── job_routes.py      # /api/jobs/* endpoints
│
├── services/
│   ├── __init__.py
│   ├── git_service.py     # Git clone/cleanup operations
│   └── job_runner.py      # Job execution engine
│
├── templates/
│   └── index.html         # Web UI
│
└── workspaces/            # Temporary job workspaces (gitignored)
```

---

## 📚 API Reference

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": "uuid-here"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Jobs

#### Create Job
```http
POST /api/jobs
Authorization: Bearer <token>
Content-Type: application/json

{
  "repo_url": "https://github.com/user/repo",
  "branch": "main"
}
```

**Response:**
```json
{
  "id": "job-uuid",
  "repo_url": "https://github.com/user/repo",
  "branch": "main",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Job Status Values

| Status | Description |
|--------|-------------|
| `pending` | Job created, waiting to start |
| `running` | Job is currently executing |
| `success` | All commands completed successfully |
| `failed` | One or more commands failed |
| `cancelled` | Job was cancelled by user |

---

## 🖼 Screenshots

### Login Page
Dark-themed authentication with Register/Login tabs.

### Dashboard
Job list with status badges, real-time updates, and action buttons.

### Logs Modal
Real-time log streaming with color-coded levels (info, warn, error).

---

## 🔒 Security Considerations

- Passwords are hashed using bcrypt with salt
- JWT tokens expire after 7 days
- Service role key should be kept secret
- Only public repositories are supported (no credential storage)
- Workspaces are cleaned up after job completion

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Supabase](https://supabase.com/) - Backend as a Service
- [GitPython](https://gitpython.readthedocs.io/) - Git operations
- [PyJWT](https://pyjwt.readthedocs.io/) - JWT implementation

---

**Made with ❤️ for the developer community**
