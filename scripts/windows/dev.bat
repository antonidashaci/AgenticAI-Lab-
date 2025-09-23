@echo off
REM AgenticAI Lab Development Script for Windows
REM Simple batch script to start development environment

echo 🚀 Starting AgenticAI Lab Development Environment
echo =================================================

REM Check if .env.local exists
if not exist ".env.local" (
    echo ⚠️  .env.local not found, copying from env.example
    copy env.example .env.local
    echo ✅ .env.local created
    echo 📝 Please edit .env.local with your configuration
    pause
)

REM Start Docker services
echo 🐳 Starting Docker services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ Failed to start Docker services
    echo Please make sure Docker Desktop is running
    pause
    exit /b 1
)

echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak > nul

REM Install dependencies if needed
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    call pnpm install
)

if not exist ".venv" (
    echo 🐍 Installing Python dependencies...
    call py -m pip install poetry
    call poetry install
)

REM Start development servers
echo 🔥 Starting development servers...
echo 📊 API will be available at: http://localhost:8000
echo 🌐 Web will be available at: http://localhost:3001
echo 📚 API docs will be available at: http://localhost:8000/docs

start /B cmd /c "cd api && poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000"
start /B cmd /c "cd web && pnpm run dev"

echo ✅ Development environment started!
echo 🛑 Press Ctrl+C to stop all services
pause
