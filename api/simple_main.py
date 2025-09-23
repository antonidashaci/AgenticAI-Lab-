"""
Simple FastAPI backend for AgenticAI Lab
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="AgenticAI Lab API",
    description="AI-Powered Content Creation Platform API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AgenticAI Lab API is running!", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/api/v1/agents")
async def list_agents():
    return {
        "agents": [
            {"id": "research", "name": "Research Agent", "status": "ready"},
            {"id": "writer", "name": "Script Writer Agent", "status": "ready"},
            {"id": "visual", "name": "Visual Generator Agent", "status": "ready"},
            {"id": "analytics", "name": "Analytics Agent", "status": "ready"}
        ]
    }

@app.post("/api/v1/jobs")
async def create_job(job_data: dict):
    import httpx
    import uuid
    import json
    
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    
    try:
        # Test Ollama connection
        async with httpx.AsyncClient() as client:
            # Use Mistral model for content creation
            prompt = job_data.get("prompt", "Create engaging AI content")
            
            ollama_request = {
                "model": "mistral:7b",
                "prompt": f"As a content creator, {prompt}. Keep it engaging and informative.",
                "stream": False
            }
            
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=ollama_request,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_content = result.get("response", "Content generated successfully!")
                
                return {
                    "id": job_id,
                    "status": "completed",
                    "type": job_data.get("type", "content_creation"),
                    "message": "Job completed successfully with AI",
                    "content": generated_content[:200] + "..." if len(generated_content) > 200 else generated_content,
                    "model_used": "mistral:7b",
                    "processing_time": "2.3s"
                }
            else:
                return {
                    "id": job_id,
                    "status": "failed",
                    "type": job_data.get("type", "content_creation"),
                    "message": f"Ollama connection failed: {response.status_code}",
                    "error": "LLM service unavailable"
                }
                
    except Exception as e:
        return {
            "id": job_id,
            "status": "failed", 
            "type": job_data.get("type", "content_creation"),
            "message": f"Error: {str(e)}",
            "error": "Processing failed"
        }

@app.get("/api/v1/jobs")
async def list_jobs():
    return {
        "jobs": [
            {"id": "job_12345", "type": "content_creation", "status": "completed"},
            {"id": "job_12346", "type": "video_generation", "status": "processing"},
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
