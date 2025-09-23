# AgenticAI Lab Setup Script for Windows
# PowerShell setup script for Windows systems

param(
    [switch]$SkipChecks,
    [switch]$NoDocker,
    [switch]$Help
)

# Show help
if ($Help) {
    Write-Host @"
AgenticAI Lab Windows Setup Script

Usage: .\setup.ps1 [options]

Options:
    -SkipChecks    Skip system requirements check
    -NoDocker      Skip Docker setup (for development without containers)
    -Help          Show this help message

Examples:
    .\setup.ps1                 # Full setup
    .\setup.ps1 -SkipChecks     # Skip requirements check
    .\setup.ps1 -NoDocker       # Setup without Docker
"@
    exit 0
}

# Set execution policy and error handling
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
$ErrorActionPreference = "Stop"

# Colors for output
$Red = [System.ConsoleColor]::Red
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Blue = [System.ConsoleColor]::Blue
$White = [System.ConsoleColor]::White

function Write-ColorText {
    param(
        [string]$Text,
        [System.ConsoleColor]$Color = $White
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Info {
    param([string]$Message)
    Write-ColorText "ℹ️  $Message" $Blue
}

function Write-Success {
    param([string]$Message)
    Write-ColorText "✅ $Message" $Green
}

function Write-Warning {
    param([string]$Message)
    Write-ColorText "⚠️  $Message" $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-ColorText "❌ $Message" $Red
}

function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Test-Requirements {
    Write-Info "Checking system requirements..."
    
    $allGood = $true
    
    # Check Windows version
    $osVersion = [System.Environment]::OSVersion.Version
    if ($osVersion.Major -lt 10) {
        Write-Error "Windows 10 or later is required"
        $allGood = $false
    } else {
        Write-Success "Windows $($osVersion.Major).$($osVersion.Minor) detected"
    }
    
    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Error "PowerShell 5.0 or later is required"
        $allGood = $false
    } else {
        Write-Success "PowerShell $($PSVersionTable.PSVersion) detected"
    }
    
    # Check Python
    if (Test-Command "py") {
        $pythonVersion = py --version 2>&1
        Write-Success "Python found: $pythonVersion"
    } elseif (Test-Command "python") {
        $pythonVersion = python --version 2>&1
        Write-Success "Python found: $pythonVersion"
    } else {
        Write-Warning "Python not found. Installing..."
        Install-Python
    }
    
    # Check Node.js
    if (Test-Command "node") {
        $nodeVersion = node --version 2>&1
        Write-Success "Node.js found: $nodeVersion"
    } else {
        Write-Warning "Node.js not found. Installing..."
        Install-NodeJS
    }
    
    # Check Git
    if (Test-Command "git") {
        $gitVersion = git --version 2>&1
        Write-Success "Git found: $gitVersion"
    } else {
        Write-Warning "Git not found. Installing..."
        Install-Git
    }
    
    # Check Docker (if not skipped)
    if (-not $NoDocker) {
        if (Test-Command "docker") {
            $dockerVersion = docker --version 2>&1
            Write-Success "Docker found: $dockerVersion"
        } else {
            Write-Warning "Docker not found. Installing..."
            Install-Docker
        }
    }
    
    if (-not $allGood) {
        Write-Error "Some requirements are not met. Please install missing components."
        exit 1
    }
}

function Install-Python {
    Write-Info "Installing Python 3.11..."
    try {
        winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
        
        # Add to PATH
        $pythonPath = "$env:USERPROFILE\AppData\Local\Programs\Python\Python311"
        $scriptsPath = "$env:USERPROFILE\AppData\Local\Programs\Python\Python311\Scripts"
        
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$pythonPath*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$pythonPath;$scriptsPath", "User")
            $env:PATH += ";$pythonPath;$scriptsPath"
        }
        
        Write-Success "Python installed successfully"
    } catch {
        Write-Error "Failed to install Python: $($_.Exception.Message)"
        exit 1
    }
}

function Install-NodeJS {
    Write-Info "Installing Node.js LTS..."
    try {
        winget install --id OpenJS.NodeJS.LTS -e --source winget --accept-package-agreements --accept-source-agreements
        
        # Add to PATH
        $nodePath = "$env:ProgramFiles\nodejs"
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$nodePath*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$nodePath", "User")
            $env:PATH += ";$nodePath"
        }
        
        Write-Success "Node.js installed successfully"
    } catch {
        Write-Error "Failed to install Node.js: $($_.Exception.Message)"
        exit 1
    }
}

function Install-Git {
    Write-Info "Installing Git..."
    try {
        winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
        
        # Add to PATH
        $gitPath = "$env:ProgramFiles\Git\cmd"
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$gitPath*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$gitPath", "User")
            $env:PATH += ";$gitPath"
        }
        
        Write-Success "Git installed successfully"
    } catch {
        Write-Error "Failed to install Git: $($_.Exception.Message)"
        exit 1
    }
}

function Install-Docker {
    Write-Info "Installing Docker Desktop..."
    try {
        winget install --id Docker.DockerDesktop -e --source winget --accept-package-agreements --accept-source-agreements
        Write-Success "Docker Desktop installed successfully"
        Write-Warning "Please restart your computer and enable WSL2 if prompted"
    } catch {
        Write-Error "Failed to install Docker Desktop: $($_.Exception.Message)"
        Write-Info "You can manually download Docker Desktop from https://www.docker.com/products/docker-desktop"
    }
}

function Install-Poetry {
    Write-Info "Installing Poetry..."
    try {
        if (Test-Command "py") {
            py -m pip install poetry
        } else {
            python -m pip install poetry
        }
        Write-Success "Poetry installed successfully"
    } catch {
        Write-Error "Failed to install Poetry: $($_.Exception.Message)"
        exit 1
    }
}

function Install-PNPM {
    Write-Info "Installing pnpm..."
    try {
        npm install -g pnpm
        Write-Success "pnpm installed successfully"
    } catch {
        Write-Error "Failed to install pnpm: $($_.Exception.Message)"
        exit 1
    }
}

function Setup-Environment {
    Write-Info "Setting up environment variables..."
    
    if (-not (Test-Path ".env.local")) {
        if (Test-Path "env.example") {
            Copy-Item "env.example" ".env.local"
            Write-Success "Environment file created (.env.local)"
            Write-Warning "Please edit .env.local with your configuration"
        } else {
            Write-Warning "env.example not found. Please create .env.local manually"
        }
    } else {
        Write-Info "Environment file already exists"
    }
}

function Install-Dependencies {
    Write-Info "Installing Python dependencies..."
    
    # Install Poetry if not present
    if (-not (Test-Command "poetry")) {
        Install-Poetry
    }
    
    # Install Python dependencies
    try {
        poetry install
        Write-Success "Python dependencies installed"
    } catch {
        Write-Error "Failed to install Python dependencies: $($_.Exception.Message)"
        exit 1
    }
    
    Write-Info "Installing Node.js dependencies..."
    
    # Install pnpm if not present
    if (-not (Test-Command "pnpm")) {
        Install-PNPM
    }
    
    # Install Node.js dependencies
    try {
        pnpm install
        Write-Success "Node.js dependencies installed"
    } catch {
        Write-Error "Failed to install Node.js dependencies: $($_.Exception.Message)"
        exit 1
    }
}

function Start-DockerServices {
    if ($NoDocker) {
        Write-Info "Skipping Docker services (NoDocker flag set)"
        return
    }
    
    Write-Info "Starting Docker services..."
    
    # Check if Docker is running
    try {
        docker info | Out-Null
    } catch {
        Write-Error "Docker is not running. Please start Docker Desktop."
        Write-Info "After starting Docker Desktop, run this script again."
        exit 1
    }
    
    # Start services
    try {
        docker-compose up -d
        Write-Info "Waiting for services to be ready..."
        Start-Sleep -Seconds 30
        Write-Success "Docker services started"
    } catch {
        Write-Error "Failed to start Docker services: $($_.Exception.Message)"
        exit 1
    }
}

function Initialize-Database {
    if ($NoDocker) {
        Write-Info "Skipping database initialization (NoDocker flag set)"
        return
    }
    
    Write-Info "Initializing database..."
    
    try {
        # Wait for PostgreSQL to be ready
        $maxAttempts = 30
        $attempt = 0
        
        do {
            $attempt++
            Write-Info "Waiting for PostgreSQL... (attempt $attempt/$maxAttempts)"
            Start-Sleep -Seconds 2
            
            try {
                docker-compose exec -T postgres pg_isready -U agenticai_user -d agenticai_dev | Out-Null
                break
            } catch {
                if ($attempt -eq $maxAttempts) {
                    throw "PostgreSQL failed to start after $maxAttempts attempts"
                }
            }
        } while ($attempt -lt $maxAttempts)
        
        # Run migrations
        Push-Location api
        poetry run alembic upgrade head
        Pop-Location
        
        Write-Success "Database initialized"
    } catch {
        Write-Error "Failed to initialize database: $($_.Exception.Message)"
        exit 1
    }
}

function Setup-Git {
    Write-Info "Setting up Git repository..."
    
    # Initialize git repository if not exists
    if (-not (Test-Path ".git")) {
        git init
        Write-Success "Git repository initialized"
    }
    
    # Set up Git configuration (if not already set)
    try {
        $userName = git config --global user.name 2>$null
        if (-not $userName) {
            $name = Read-Host "Enter your Git username"
            git config --global user.name $name
        }
        
        $userEmail = git config --global user.email 2>$null
        if (-not $userEmail) {
            $email = Read-Host "Enter your Git email"
            git config --global user.email $email
        }
        
        Write-Success "Git configuration complete"
    } catch {
        Write-Warning "Git configuration failed, but continuing..."
    }
    
    # Install pre-commit hooks
    try {
        poetry run pre-commit install
        Write-Success "Git hooks installed"
    } catch {
        Write-Warning "Failed to install Git hooks, but continuing..."
    }
}

function Test-Installation {
    Write-Info "Verifying installation..."
    
    $allGood = $true
    
    # Check if services are running (if Docker is used)
    if (-not $NoDocker) {
        try {
            $services = docker-compose ps
            if ($services -match "Up") {
                Write-Success "Docker services are running"
            } else {
                Write-Warning "Some Docker services may not be running"
                $allGood = $false
            }
        } catch {
            Write-Warning "Could not check Docker services status"
            $allGood = $false
        }
    }
    
    # Check if files exist
    $requiredFiles = @(
        "pyproject.toml",
        "package.json",
        "docker-compose.yml",
        ".env.local"
    )
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Success "$file exists"
        } else {
            Write-Warning "$file is missing"
            $allGood = $false
        }
    }
    
    if ($allGood) {
        Write-Success "Installation verification completed successfully"
    } else {
        Write-Warning "Some issues were found, but setup may still work"
    }
}

function Show-NextSteps {
    Write-Host ""
    Write-ColorText "🎉 Setup Complete!" $Green
    Write-Host "==================="
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Edit .env.local with your API keys and configuration"
    Write-Host "2. Start development servers:"
    Write-ColorText "   .\scripts\windows\dev.bat" $Yellow
    Write-Host "   OR"
    Write-ColorText "   make dev" $Yellow
    Write-Host "3. Open http://localhost:3001 for the web interface"
    Write-Host "4. Open http://localhost:8000/docs for the API documentation"
    Write-Host ""
    Write-Host "Useful commands:"
    Write-Host "- make dev          # Start development servers"
    Write-Host "- make docker-up    # Start Docker services"
    Write-Host "- make docker-down  # Stop Docker services"
    Write-Host "- make test         # Run tests"
    Write-Host "- make help         # Show all available commands"
    Write-Host ""
    Write-Host "For more information, see the README.md file."
}

# Main execution
function Main {
    Write-ColorText "🚀 AgenticAI Lab Windows Setup Script" $Blue
    Write-Host "======================================"
    Write-Host ""
    
    try {
        if (-not $SkipChecks) {
            Test-Requirements
        }
        
        Setup-Environment
        Install-Dependencies
        Start-DockerServices
        Initialize-Database
        Setup-Git
        Test-Installation
        Show-NextSteps
        
        Write-Success "Setup completed successfully!"
        
    } catch {
        Write-Error "Setup failed: $($_.Exception.Message)"
        Write-Host ""
        Write-Host "For help, run: .\setup.ps1 -Help"
        exit 1
    }
}

# Run main function
Main
