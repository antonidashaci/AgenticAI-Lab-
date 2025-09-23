"""
Base Agent Class

Abstract base class for all AI agents in the AgenticAI Lab system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum
import uuid
import logging
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AgentCapability(str, Enum):
    """Agent capability enumeration."""
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    AUDIO_GENERATION = "audio_generation"
    VIDEO_PROCESSING = "video_processing"
    WEB_SCRAPING = "web_scraping"
    DATA_ANALYSIS = "data_analysis"
    QUALITY_ASSURANCE = "quality_assurance"
    CONTENT_DEPLOYMENT = "content_deployment"
    PERFORMANCE_ANALYTICS = "performance_analytics"


class ResourceSpec(BaseModel):
    """Resource requirements specification."""
    cpu_cores: int = Field(default=1, ge=1)
    memory_gb: float = Field(default=2.0, ge=0.5)
    gpu_memory_gb: Optional[float] = Field(default=None, ge=0.0)
    disk_space_gb: float = Field(default=1.0, ge=0.1)
    network_bandwidth_mbps: float = Field(default=10.0, ge=1.0)


class RateLimitSpec(BaseModel):
    """Rate limiting specification."""
    requests_per_minute: int = Field(default=60, ge=1)
    requests_per_hour: int = Field(default=1000, ge=1)
    concurrent_requests: int = Field(default=5, ge=1)


class RetryPolicy(BaseModel):
    """Retry policy specification."""
    max_attempts: int = Field(default=3, ge=1)
    backoff_factor: float = Field(default=2.0, ge=1.0)
    initial_delay_seconds: float = Field(default=1.0, ge=0.1)
    max_delay_seconds: float = Field(default=300.0, ge=1.0)


class MonitoringConfig(BaseModel):
    """Monitoring configuration."""
    enable_metrics: bool = True
    enable_logging: bool = True
    log_level: str = "INFO"
    metrics_interval_seconds: int = Field(default=60, ge=1)


class AgentConfig(BaseModel):
    """Agent configuration."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    version: str = "1.0.0"
    description: Optional[str] = None
    capabilities: List[AgentCapability]
    resource_requirements: ResourceSpec = Field(default_factory=ResourceSpec)
    rate_limits: RateLimitSpec = Field(default_factory=RateLimitSpec)
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    custom_config: Dict[str, Any] = Field(default_factory=dict)


class AgentInput(BaseModel):
    """Base input model for agent tasks."""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    job_id: Optional[str] = None
    data: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentOutput(BaseModel):
    """Base output model for agent results."""
    task_id: str
    agent_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_seconds: float
    tokens_used: int = 0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    
    This class provides the common interface and functionality that all
    specialized agents must implement.
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the agent with configuration.
        
        Args:
            config: Agent configuration object
        """
        self.config = config
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(f"agent.{config.name}")
        self._setup_logging()
        
        # Runtime state
        self.current_task: Optional[str] = None
        self.last_activity: datetime = datetime.utcnow()
        self.total_tasks_processed: int = 0
        self.total_errors: int = 0
        
        # Initialize agent-specific components
        self._initialize()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(self.config.monitoring.log_level)
    
    @abstractmethod
    def _initialize(self) -> None:
        """Initialize agent-specific components."""
        pass
    
    @abstractmethod
    async def process(self, input_data: AgentInput) -> AgentOutput:
        """
        Process a task with the given input data.
        
        Args:
            input_data: Input data for the task
            
        Returns:
            AgentOutput: Result of the task processing
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """
        Get the list of capabilities this agent supports.
        
        Returns:
            List of agent capabilities
        """
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the agent.
        
        Returns:
            Dictionary containing health status information
        """
        try:
            # Basic health checks
            health_data = {
                "agent_id": self.config.id,
                "agent_name": self.config.name,
                "status": self.status.value,
                "last_activity": self.last_activity.isoformat(),
                "total_tasks_processed": self.total_tasks_processed,
                "total_errors": self.total_errors,
                "uptime_seconds": (datetime.utcnow() - self.last_activity).total_seconds(),
                "capabilities": [cap.value for cap in self.get_capabilities()],
                "healthy": True
            }
            
            # Agent-specific health checks
            agent_health = await self._agent_health_check()
            health_data.update(agent_health)
            
            return health_data
            
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return {
                "agent_id": self.config.id,
                "agent_name": self.config.name,
                "status": AgentStatus.ERROR.value,
                "healthy": False,
                "error": str(e)
            }
    
    async def _agent_health_check(self) -> Dict[str, Any]:
        """
        Perform agent-specific health checks.
        
        Returns:
            Dictionary containing agent-specific health information
        """
        return {}
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the agent.
        
        Returns:
            Dictionary containing performance metrics
        """
        return {
            "agent_id": self.config.id,
            "agent_name": self.config.name,
            "status": self.status.value,
            "total_tasks_processed": self.total_tasks_processed,
            "total_errors": self.total_errors,
            "error_rate": self.total_errors / max(self.total_tasks_processed, 1),
            "last_activity": self.last_activity.isoformat(),
            "current_task": self.current_task
        }
    
    def _update_status(self, status: AgentStatus, task_id: Optional[str] = None) -> None:
        """
        Update agent status and current task.
        
        Args:
            status: New agent status
            task_id: Current task ID (if any)
        """
        self.status = status
        self.current_task = task_id
        self.last_activity = datetime.utcnow()
        
        self.logger.info(f"Status updated to {status.value}, task: {task_id}")
    
    def _log_task_start(self, task_id: str, input_data: AgentInput) -> None:
        """Log task start."""
        self.logger.info(f"Starting task {task_id} for user {input_data.user_id}")
        self._update_status(AgentStatus.BUSY, task_id)
    
    def _log_task_completion(self, task_id: str, success: bool, execution_time: float) -> None:
        """Log task completion."""
        if success:
            self.total_tasks_processed += 1
            self.logger.info(f"Task {task_id} completed successfully in {execution_time:.2f}s")
        else:
            self.total_errors += 1
            self.logger.error(f"Task {task_id} failed after {execution_time:.2f}s")
        
        self._update_status(AgentStatus.IDLE)
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(id={self.config.id}, name={self.config.name}, status={self.status.value})"
