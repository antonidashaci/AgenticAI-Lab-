#!/usr/bin/env python3
"""
Model Download Script

Downloads and sets up AI models for AgenticAI Lab.
"""

import os
import sys
import requests
import subprocess
from pathlib import Path
import json
import hashlib
from tqdm import tqdm
import argparse

# Model configurations
MODELS_CONFIG = {
    "ollama": {
        "llama3.1:8b": {
            "description": "Llama 3.1 8B - General purpose LLM",
            "size": "4.7GB",
            "priority": 1
        },
        "llama3.1:70b": {
            "description": "Llama 3.1 70B - Large context LLM", 
            "size": "40GB",
            "priority": 3
        },
        "deepseek-coder:6.7b": {
            "description": "DeepSeek Coder 6.7B - Code generation",
            "size": "3.8GB", 
            "priority": 2
        },
        "mistral:7b": {
            "description": "Mistral 7B - Fast inference",
            "size": "4.1GB",
            "priority": 2
        }
    },
    "huggingface": {
        "stabilityai/stable-diffusion-xl-base-1.0": {
            "description": "SDXL Base - Image generation",
            "size": "6.9GB",
            "priority": 1,
            "files": [
                "model_index.json",
                "scheduler/scheduler_config.json",
                "text_encoder/config.json",
                "text_encoder/pytorch_model.bin",
                "text_encoder_2/config.json", 
                "text_encoder_2/pytorch_model.bin",
                "tokenizer/merges.txt",
                "tokenizer/special_tokens_map.json",
                "tokenizer/tokenizer_config.json",
                "tokenizer/vocab.json",
                "tokenizer_2/merges.txt",
                "tokenizer_2/special_tokens_map.json",
                "tokenizer_2/tokenizer_config.json",
                "tokenizer_2/vocab.json",
                "unet/config.json",
                "unet/diffusion_pytorch_model.safetensors",
                "vae/config.json",
                "vae/diffusion_pytorch_model.safetensors"
            ]
        },
        "openai/whisper-large-v3": {
            "description": "Whisper Large V3 - Speech to text",
            "size": "1.5GB",
            "priority": 2,
            "files": [
                "config.json",
                "preprocessor_config.json",
                "pytorch_model.bin",
                "tokenizer.json",
                "vocab.json"
            ]
        }
    }
}

class ModelDownloader:
    def __init__(self, models_dir: str = "./models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
    def download_ollama_models(self, models: list = None):
        """Download Ollama models."""
        print("🦙 Downloading Ollama models...")
        
        # Check if Ollama is available
        try:
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Ollama not found. Installing Ollama...")
                self._install_ollama()
        except FileNotFoundError:
            print("❌ Ollama not found. Installing Ollama...")
            self._install_ollama()
        
        # Download models
        ollama_models = models or list(MODELS_CONFIG["ollama"].keys())
        
        for model in ollama_models:
            if model in MODELS_CONFIG["ollama"]:
                config = MODELS_CONFIG["ollama"][model]
                print(f"\n📥 Downloading {model}")
                print(f"   Description: {config['description']}")
                print(f"   Size: {config['size']}")
                
                try:
                    result = subprocess.run(
                        ["ollama", "pull", model],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        print(f"✅ {model} downloaded successfully")
                    else:
                        print(f"❌ Failed to download {model}: {result.stderr}")
                        
                except Exception as e:
                    print(f"❌ Error downloading {model}: {str(e)}")
            else:
                print(f"⚠️  Unknown model: {model}")
    
    def _install_ollama(self):
        """Install Ollama on Windows."""
        print("📦 Installing Ollama...")
        
        try:
            # Download Ollama installer
            url = "https://ollama.ai/download/OllamaSetup.exe"
            installer_path = self.models_dir / "OllamaSetup.exe"
            
            print("📥 Downloading Ollama installer...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(installer_path, 'wb') as f, tqdm(
                desc="Ollama Installer",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
            
            print("🚀 Running Ollama installer...")
            print("   Please follow the installer instructions.")
            print("   After installation, restart this script.")
            
            # Run installer
            subprocess.run([str(installer_path)], check=True)
            
        except Exception as e:
            print(f"❌ Failed to install Ollama: {str(e)}")
            print("   Please install Ollama manually from https://ollama.ai")
    
    def download_huggingface_models(self, models: list = None):
        """Download Hugging Face models."""
        print("\n🤗 Downloading Hugging Face models...")
        
        try:
            from huggingface_hub import snapshot_download
        except ImportError:
            print("📦 Installing huggingface_hub...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "huggingface_hub"
            ])
            from huggingface_hub import snapshot_download
        
        hf_models = models or list(MODELS_CONFIG["huggingface"].keys())
        
        for model in hf_models:
            if model in MODELS_CONFIG["huggingface"]:
                config = MODELS_CONFIG["huggingface"][model]
                print(f"\n📥 Downloading {model}")
                print(f"   Description: {config['description']}")
                print(f"   Size: {config['size']}")
                
                # Create model directory
                model_dir = self.models_dir / model.replace("/", "_")
                model_dir.mkdir(exist_ok=True)
                
                try:
                    # Download model
                    snapshot_download(
                        repo_id=model,
                        local_dir=str(model_dir),
                        allow_patterns=config.get("files", ["*"]),
                        cache_dir=str(self.models_dir / "cache")
                    )
                    
                    print(f"✅ {model} downloaded successfully")
                    
                except Exception as e:
                    print(f"❌ Failed to download {model}: {str(e)}")
            else:
                print(f"⚠️  Unknown model: {model}")
    
    def check_disk_space(self):
        """Check available disk space."""
        import shutil
        
        total, used, free = shutil.disk_usage(self.models_dir)
        free_gb = free // (1024**3)
        
        print(f"💾 Available disk space: {free_gb} GB")
        
        # Calculate total size needed
        total_size = 0
        for category in MODELS_CONFIG.values():
            for model_config in category.values():
                size_str = model_config["size"]
                size_gb = float(size_str.replace("GB", ""))
                total_size += size_gb
        
        print(f"📊 Total models size: {total_size:.1f} GB")
        
        if free_gb < total_size:
            print("⚠️  Warning: Insufficient disk space!")
            return False
        
        return True
    
    def list_available_models(self):
        """List all available models."""
        print("\n📋 Available Models:")
        print("=" * 50)
        
        for category, models in MODELS_CONFIG.items():
            print(f"\n{category.upper()}:")
            for model_name, config in models.items():
                priority = "⭐" * config["priority"]
                print(f"  {priority} {model_name}")
                print(f"     {config['description']}")
                print(f"     Size: {config['size']}")
    
    def download_priority_models(self, priority: int = 1):
        """Download models by priority level."""
        print(f"\n🎯 Downloading priority {priority} models...")
        
        ollama_models = []
        hf_models = []
        
        for model_name, config in MODELS_CONFIG["ollama"].items():
            if config["priority"] <= priority:
                ollama_models.append(model_name)
        
        for model_name, config in MODELS_CONFIG["huggingface"].items():
            if config["priority"] <= priority:
                hf_models.append(model_name)
        
        if ollama_models:
            self.download_ollama_models(ollama_models)
        
        if hf_models:
            self.download_huggingface_models(hf_models)


def main():
    parser = argparse.ArgumentParser(description="Download AI models for AgenticAI Lab")
    parser.add_argument("--models-dir", default="./models", 
                       help="Directory to store models")
    parser.add_argument("--priority", type=int, choices=[1, 2, 3], default=1,
                       help="Download models by priority (1=essential, 2=recommended, 3=optional)")
    parser.add_argument("--list", action="store_true",
                       help="List available models")
    parser.add_argument("--ollama-only", action="store_true",
                       help="Download only Ollama models")
    parser.add_argument("--hf-only", action="store_true", 
                       help="Download only Hugging Face models")
    parser.add_argument("--check-space", action="store_true",
                       help="Check disk space requirements")
    
    args = parser.parse_args()
    
    downloader = ModelDownloader(args.models_dir)
    
    if args.list:
        downloader.list_available_models()
        return
    
    if args.check_space:
        downloader.check_disk_space()
        return
    
    print("🚀 AgenticAI Lab Model Downloader")
    print("=" * 40)
    
    # Check disk space
    if not downloader.check_disk_space():
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Download cancelled")
            return
    
    # Download models
    if args.ollama_only:
        downloader.download_ollama_models()
    elif args.hf_only:
        downloader.download_huggingface_models()
    else:
        downloader.download_priority_models(args.priority)
    
    print("\n🎉 Model download completed!")
    print("\nNext steps:")
    print("1. Start Docker services: docker-compose up -d")
    print("2. Start development servers: make dev")
    print("3. Open http://localhost:3001")


if __name__ == "__main__":
    main()
