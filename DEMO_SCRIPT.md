# CI/CD Server Demo Script (5-7 minutes)

## Opening (30 seconds)
**[Show desktop with browser open]**

"Welcome to the CI/CD Automation Server - a lightweight, self-hosted pipeline runner built with Flask and Supabase. Today I'll walk you through creating an account, running a pipeline, and viewing real-time analytics."

---

## Section 1: Authentication (1 minute)

**[Navigate to https://ci-cd-server-0lka.onrender.com]**

"First, let's create an account. I'll click on 'Create Account' tab."

**[Click Create Account tab]**

"Enter an email address..."
- Type: `demo@example.com`

"...and a password."
- Type: `DemoPassword123`

**[Click Create Account button]**

"Great! We're now logged in. You can see the dashboard with options to create a new pipeline."

---

## Section 2: Creating a Pipeline Job (1.5 minutes)

**[Show the "New Pipeline" card]**

"Now let's create our first CI/CD job. I'll enter a GitHub repository URL. Let me use a popular open-source project."

**[Click on repo URL input]**
- Type: `https://github.com/torvalds/linux`

"I'll set the branch to main..."
**[Click branch input, clear it, type: `main`]**

"Now click Run to start the pipeline."
**[Click Run button]**

**[Wait 2-3 seconds for job to appear]**

"Perfect! The job has been created and is now in 'pending' status. You can see it in the Recent Pipelines section with:
- Repository name
- Branch
- Status badge
- Timestamp
- Action buttons"

**[Point to the job entry]**

"Let me click on 'Logs' to see real-time execution."

**[Click Logs button]**

**[Show logs modal with live output]**

"Here we can see the pipeline logs in real-time. The system is:
1. Cloning the repository
2. Detecting the project type
3. Running appropriate build commands
4. Streaming output as it happens"

**[Close logs modal]**

---

## Section 3: Job Management (1 minute)

**[Show the job in the list]**

"While the job is running, we have several options:
- View logs (which we just did)
- Cancel the job if needed
- Once complete, retry if it fails
- Delete the job"

**[Wait for job status to change to 'success' or 'failed']**

"The job has completed! Notice the status changed and the status badge updated. If this was a failed job, we could click 'Retry' to run it again."

---

## Section 4: Analytics Dashboard (2 minutes)

**[Click Analytics link in the header]**

"Now let's check out the Analytics dashboard. This gives us real-time insights into our CI/CD pipeline performance."

**[Wait for dashboard to load]**

"The dashboard shows several key metrics:

**Top Row - KPI Cards:**
- Total Jobs: Number of pipelines executed
- Success Rate: Percentage of successful runs
- Failed: Count of failed jobs
- Running: Currently executing jobs
- Avg Duration: Average execution time
- Users: Number of registered users"

**[Scroll down slightly]**

"**Row 1 - Charts:**
- Pipeline Throughput: Shows job volume over time
- Status Distribution: Pie chart of success/failed/running jobs"

**[Continue scrolling]**

"**Row 2 - Analytics:**
- Weekly Activity Heatmap: Shows when jobs run (by day and hour)
- Duration by Status: Box plot comparing execution times
- Hourly Distribution: Bar chart of jobs by hour"

**[Continue scrolling]**

"**Row 3 - Performance:**
- Repository Performance: Top repositories by job count
- Success vs Failure Trend: Line chart showing success/failure over time"

**[Continue scrolling]**

"**Row 4 - Details:**
- Recent Pipelines: Table of latest jobs with details
- Live Logs: Real-time log feed from active jobs"

---

## Section 5: API & Integration (1 minute)

**[Go back to main app]**

"Beyond the web interface, this server provides a full REST API for integration with other tools:

**Authentication Endpoints:**
- POST /api/auth/register - Create new user
- POST /api/auth/login - Get JWT token
- GET /api/auth/me - Get current user

**Job Management:**
- POST /api/jobs - Create new job
- GET /api/jobs - List all jobs
- GET /api/jobs/{id} - Get job details
- GET /api/jobs/{id}/logs - Stream logs
- POST /api/jobs/{id}/cancel - Cancel running job
- POST /api/jobs/{id}/retry - Retry failed job
- DELETE /api/jobs/{id} - Delete job

You can use these endpoints with cURL, Postman, or any HTTP client."

---

## Section 6: Key Features Summary (30 seconds)

**[Back to dashboard]**

"Let me recap the key features:

✅ **JWT Authentication** - Secure user management
✅ **Git Integration** - Clone and run any public repository
✅ **Real-time Logs** - Stream execution output live
✅ **Auto-Detection** - Automatically detect Python, Node.js, Java, Go, Rust projects
✅ **Job Management** - Full CRUD operations via UI and API
✅ **Analytics Dashboard** - Real-time performance metrics
✅ **Retry & Cancel** - Manage running and failed jobs
✅ **Cloud Ready** - Deployed on Render, scales automatically"

---

## Closing (30 seconds)

"The CI/CD Server is perfect for:
- Personal projects
- Team automation
- Learning CI/CD concepts
- Prototyping deployment pipelines

The entire codebase is open source on GitHub at:
**github.com/Aamod007/CI-CD-Server**

Thanks for watching! If you have questions, check out the README for detailed documentation."

---

## Demo Tips for Recording:

1. **Pre-create a job** before recording so you have one in the list
2. **Use a small repository** (not Linux kernel) for faster demo - try:
   - `https://github.com/octocat/Hello-World`
   - `https://github.com/facebook/react` (if you want something substantial)
3. **Have the analytics dashboard ready** - refresh it before recording
4. **Use browser zoom** (Ctrl/Cmd + +) to make text larger for video
5. **Speak clearly and pause** between sections for editing
6. **Record in 1080p or higher** for clarity
7. **Use a screen recording tool** like OBS Studio (free) or ScreenFlow (Mac)

## Recording Checklist:

- [ ] Test login/registration flow
- [ ] Create a test job
- [ ] View logs while job runs
- [ ] Show job completion
- [ ] Navigate to analytics
- [ ] Explain each dashboard section
- [ ] Show API endpoints documentation
- [ ] Mention GitHub repo link
- [ ] Test on mobile (optional)

---

**Total Runtime: 5-7 minutes**
