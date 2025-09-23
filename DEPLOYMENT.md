# 🚀 AgenticAI Lab Deployment Guide

## Quick Start with CodeRabbit AI Review

This repository is configured with **CodeRabbit AI** for automated code reviews. Here's how to get started:

### 1. Prerequisites
- Docker Desktop installed
- Node.js 20+ and pnpm
- Python 3.11+ and Poetry
- Git configured

### 2. Clone and Setup
```bash
git clone https://github.com/YOUR_USERNAME/agenticai-lab.git
cd agenticai-lab

# Install dependencies
pnpm install
poetry install

# Start infrastructure
docker-compose up -d postgres redis qdrant ollama

# Start services
pnpm run dev:web    # Frontend on :3001
poetry run uvicorn api.simple_main:app --reload --port 8001  # Backend on :8001
```

### 3. CodeRabbit Integration

#### For Public Repositories (FREE):
1. Go to [GitHub Marketplace - CodeRabbit](https://github.com/marketplace/coderabbit-ai)
2. Click "Set up a plan" → "Free for public repositories"
3. Select this repository and install
4. CodeRabbit will automatically review all new PRs

#### For CLI Reviews (Coming to Windows):
```bash
# When Windows support is available:
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit review --plain  # For AI agent integration
```

### 4. Creating Your First PR with AI Review

```bash
# Create feature branch
git checkout -b feature/your-improvement
git add .
git commit -m "Your improvement description"
git push origin feature/your-improvement

# Create PR on GitHub - CodeRabbit will automatically review!
```

### 5. AI Models Included
- **Mistral 7B** (4.4GB) - General content creation
- **CodeLlama 13B** (7.4GB) - Code generation and review
- **Llama 3.2 3B** (2.0GB) - Fast responses

### 6. System Architecture
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Next.js   │───▶│   FastAPI    │───▶│   Ollama    │
│  Frontend   │    │   Backend    │    │ LLM Models  │
│  (Port 3001)│    │ (Port 8001)  │    │(Port 11434) │
└─────────────┘    └──────────────┘    └─────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  PostgreSQL  │
                   │    Redis     │
                   │   Qdrant     │
                   │ (Docker)     │
                   └──────────────┘
```

### 7. Health Monitoring
- Basic health: `http://localhost:8001/health`
- Detailed health: `http://localhost:8001/health/detailed`
- Dashboard: `http://localhost:3001/dashboard`

### 8. CodeRabbit Configuration
The `.coderabbit.yml` file configures:
- ✅ Security vulnerability detection
- ✅ Performance optimization suggestions  
- ✅ AI integration best practices
- ✅ Docker security checks
- ✅ Python/TypeScript specific reviews

## 🤖 AI-Powered Development Workflow

1. **Write Code** → AI assistance (Cursor, Claude, etc.)
2. **Pre-commit Review** → CodeRabbit CLI (coming to Windows)
3. **Create PR** → Automatic CodeRabbit review
4. **Iterate** → One-click fixes and improvements
5. **Merge** → Production-ready code

**Ready to revolutionize your development workflow with AI! 🚀**
