"""
Health Check Service for AgenticAI Lab
Provides comprehensive system health monitoring
"""

import asyncio
import httpx
import psutil
from typing import Dict, Any
from datetime import datetime

class HealthChecker:
    """System health monitoring service"""
    
    def __init__(self):
        self.services = {
            "ollama": "http://localhost:11434/api/health",
            "postgres": None,  # Will check via database connection
            "redis": None,     # Will check via redis connection
            "qdrant": "http://localhost:6333/health"
        }
    
    async def check_all_services(self) -> Dict[str, Any]:
        """Check health of all system services"""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": "healthy",
            "services": {},
            "system": await self._check_system_resources()
        }
        
        # Check HTTP services
        for service_name, url in self.services.items():
            if url:
                results["services"][service_name] = await self._check_http_service(url)
        
        # Check database connections
        results["services"]["postgres"] = await self._check_postgres()
        results["services"]["redis"] = await self._check_redis()
        
        # Determine overall status
        unhealthy_services = [
            name for name, status in results["services"].items() 
            if status.get("status") != "healthy"
        ]
        
        if unhealthy_services:
            results["overall_status"] = "degraded"
            results["unhealthy_services"] = unhealthy_services
        
        return results
    
    async def _check_http_service(self, url: str) -> Dict[str, Any]:
        """Check HTTP service health"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                return {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def _check_postgres(self) -> Dict[str, Any]:
        """Check PostgreSQL connection"""
        # This is a placeholder - would need actual DB connection
        return {"status": "healthy", "note": "Mock check - implement with SQLAlchemy"}
    
    async def _check_redis(self) -> Dict[str, Any]:
        """Check Redis connection"""
        # This is a placeholder - would need actual Redis connection
        return {"status": "healthy", "note": "Mock check - implement with redis-py"}
    
    async def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }

# Global health checker instance
health_checker = HealthChecker()
