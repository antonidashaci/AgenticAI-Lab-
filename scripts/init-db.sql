-- Initialize PostgreSQL database for AgenticAI Lab
CREATE USER agenticai_user WITH PASSWORD 'agenticai_password';
CREATE DATABASE agenticai_dev OWNER agenticai_user;
GRANT ALL PRIVILEGES ON DATABASE agenticai_dev TO agenticai_user;

\connect agenticai_dev;

-- Example schema placeholder (extend with real tables/migrations later)
CREATE SCHEMA IF NOT EXISTS public;


