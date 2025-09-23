#!/bin/bash

# AgenticAI Lab Setup Script
# Initial setup script for Unix-like systems (Linux, macOS, WSL)

set -e  # Exit on any error

echo "🚀 AgenticAI Lab Setup Script"
echo "============================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION found"
    else
        log_error "Python 3 is not installed. Please install Python 3.11 or later."
        exit 1
    fi
    
    # Check Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        log_success "Node.js $NODE_VERSION found"
    else
        log_error "Node.js is not installed. Please install Node.js 20.10.0 or later."
        exit 1
    fi
    
    # Check Docker
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        log_success "Docker $DOCKER_VERSION found"
    else
        log_error "Docker is not installed. Please install Docker Desktop."
        exit 1
    fi
    
    # Check Git
    if command_exists git; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        log_success "Git $GIT_VERSION found"
    else
        log_error "Git is not installed. Please install Git."
        exit 1
    fi
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    # Check if Poetry is installed
    if ! command_exists poetry; then
        log_info "Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    # Install dependencies with Poetry
    poetry install
    log_success "Python dependencies installed"
}

# Install Node.js dependencies
install_node_deps() {
    log_info "Installing Node.js dependencies..."
    
    # Check if pnpm is installed
    if ! command_exists pnpm; then
        log_info "Installing pnpm..."
        npm install -g pnpm
    fi
    
    # Install dependencies with pnpm
    pnpm install
    log_success "Node.js dependencies installed"
}

# Setup environment variables
setup_env() {
    log_info "Setting up environment variables..."
    
    if [ ! -f .env.local ]; then
        cp env.example .env.local
        log_success "Environment file created (.env.local)"
        log_warning "Please edit .env.local with your configuration"
    else
        log_info "Environment file already exists"
    fi
}

# Start Docker services
start_docker() {
    log_info "Starting Docker services..."
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    # Start services
    docker-compose up -d
    
    log_info "Waiting for services to be ready..."
    sleep 30
    
    log_success "Docker services started"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    # Wait for PostgreSQL to be ready
    until docker-compose exec postgres pg_isready -U agenticai_user -d agenticai_dev; do
        log_info "Waiting for PostgreSQL..."
        sleep 2
    done
    
    # Run migrations
    cd api && poetry run alembic upgrade head
    cd ..
    
    log_success "Database migrations completed"
}

# Download AI models
download_models() {
    log_info "Setting up AI models..."
    
    # Create models directories
    mkdir -p models/{ollama,sdxl,whisper,xtts}
    
    # Pull Ollama models
    if command_exists ollama; then
        log_info "Pulling Ollama models..."
        ollama pull llama3.1:8b
        ollama pull llama3.1:70b
        log_success "Ollama models downloaded"
    else
        log_warning "Ollama not found. Models will be downloaded when Docker container starts."
    fi
}

# Setup Git hooks
setup_git() {
    log_info "Setting up Git hooks..."
    
    # Initialize git repository if not exists
    if [ ! -d .git ]; then
        git init
        log_success "Git repository initialized"
    fi
    
    # Install pre-commit hooks
    poetry run pre-commit install
    log_success "Git hooks installed"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        log_success "Docker services are running"
    else
        log_error "Some Docker services are not running"
    fi
    
    # Check if API is accessible
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        log_success "API is accessible"
    else
        log_warning "API is not accessible yet (this is normal on first setup)"
    fi
    
    log_success "Setup completed successfully!"
}

# Print next steps
print_next_steps() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "================="
    echo ""
    echo "Next steps:"
    echo "1. Edit .env.local with your API keys and configuration"
    echo "2. Start development servers: make dev"
    echo "3. Open http://localhost:3001 for the web interface"
    echo "4. Open http://localhost:8000/docs for the API documentation"
    echo ""
    echo "Useful commands:"
    echo "- make dev          # Start development servers"
    echo "- make docker-up    # Start Docker services"
    echo "- make docker-down  # Stop Docker services"
    echo "- make test         # Run tests"
    echo "- make help         # Show all available commands"
    echo ""
    echo "For more information, see the README.md file."
}

# Main execution
main() {
    check_requirements
    setup_env
    install_python_deps
    install_node_deps
    start_docker
    run_migrations
    download_models
    setup_git
    verify_installation
    print_next_steps
}

# Run main function
main "$@"
