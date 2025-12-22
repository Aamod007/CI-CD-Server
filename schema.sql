-- Run this in your Supabase SQL Editor

-- Users table (for raw JWT auth)
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
  status text default 'pending', -- pending, running, success, failed, cancelled
  created_at timestamptz default now(),
  started_at timestamptz,
  finished_at timestamptz
);

-- Job logs table
create table if not exists job_logs (
  id uuid primary key default gen_random_uuid(),
  job_id uuid references jobs(id) on delete cascade,
  message text,
  level text default 'info', -- info, error, warn
  created_at timestamptz default now()
);

-- Indexes for performance
create index if not exists idx_jobs_user_id on jobs(user_id);
create index if not exists idx_jobs_status on jobs(status);
create index if not exists idx_job_logs_job_id on job_logs(job_id);
create index if not exists idx_users_email on users(email);
