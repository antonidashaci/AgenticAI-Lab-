#!/usr/bin/env python3
"""
Ultra Simple Backend for AgenticAI Lab
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uuid
import asyncio

app = FastAPI(title="AgenticAI Test API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AgenticAI Test API is working!", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/api/v1/agents")
async def list_agents():
    return {
        "agents": [
            {"id": "mistral", "name": "Mistral 7B", "status": "ready"},
            {"id": "codellama", "name": "Code Llama 13B", "status": "ready"},
            {"id": "llama", "name": "Llama 3.2 3B", "status": "ready"}
        ]
    }

@app.post("/api/v1/jobs")
async def create_job(job_data: dict):
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    prompt = job_data.get("prompt", "Hello AI!")
    
    print(f"Creating job {job_id} with prompt: {prompt}")
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            ollama_request = {
                "model": "mistral:7b",
                "prompt": f"As a helpful AI assistant: {prompt}",
                "stream": False
            }
            
            print("Sending request to Ollama...")
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=ollama_request
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("response", "AI generated content!")
                
                print(f"Success! Generated content: {content[:100]}...")
                
                return {
                    "id": job_id,
                    "status": "completed",
                    "type": "content_creation",
                    "message": "Job completed successfully!",
                    "content": content[:300] + "..." if len(content) > 300 else content,
                    "model": "mistral:7b"
                }
            else:
                print(f"Ollama error: {response.status_code}")
                return {
                    "id": job_id,
                    "status": "failed",
                    "message": f"Ollama API error: {response.status_code}",
                    "error": "LLM service error"
                }
                
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            "id": job_id,
            "status": "failed", 
            "message": f"Error: {str(e)}",
            "error": "Processing failed"
        }

@app.get("/api/v1/jobs")
async def list_jobs():
    return {
        "jobs": [
            {"id": "job_sample1", "type": "content_creation", "status": "completed"},
            {"id": "job_sample2", "type": "content_creation", "status": "processing"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting AgenticAI Test Server...")
    print("Frontend: http://localhost:3001")
    print("Backend: http://localhost:8001")
    print("Health: http://localhost:8001/health")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
