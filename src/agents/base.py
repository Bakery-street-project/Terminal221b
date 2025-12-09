"""Base agent interface for Terminal221b."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AgentCapability(str, Enum):
    """Agent capabilities that can be enabled/disabled by license tier."""
    
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    IMAGE_GENERATION = "image_generation"
    BLOCKCHAIN_OPS = "blockchain_ops"
    MULTI_AGENT = "multi_agent"


class AgentMessage(BaseModel):
    """Message in agent conversation."""
    
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None


class AgentContext(BaseModel):
    """Context passed to agent for execution."""
    
    messages: List[AgentMessage] = []
    max_tokens: int = 1000
    temperature: float = 0.7
    capabilities: List[AgentCapability] = []
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AgentResult:
    """Result from agent execution."""
    
    success: bool
    output: str
    tokens_used: int = 0
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BaseAgent(ABC):
    """Base class for all Terminal221b agents.
    
    Agents are the core execution units in the PAO system.
    Each agent specializes in a particular domain and can
    collaborate with other agents through the coordinator.
    """
    
    name: str = "base"
    description: str = "Base agent interface"
    required_capabilities: List[AgentCapability] = []
    
    def __init__(self, context: Optional[AgentContext] = None):
        """Initialize agent with optional context.
        
        Args:
            context: Execution context with capabilities and settings
        """
        self.context = context or AgentContext()
        self._validate_capabilities()
    
    def _validate_capabilities(self) -> None:
        """Validate that required capabilities are available."""
        for cap in self.required_capabilities:
            if cap not in self.context.capabilities:
                raise PermissionError(
                    f"Agent '{self.name}' requires capability '{cap.value}' "
                    "which is not available in current license tier."
                )
    
    @abstractmethod
    async def execute(self, prompt: str) -> AgentResult:
        """Execute agent with given prompt.
        
        Args:
            prompt: User prompt to process
            
        Returns:
            AgentResult with output and metadata
        """
        pass
    
    @abstractmethod
    async def stream(self, prompt: str):
        """Stream agent output token by token.
        
        Args:
            prompt: User prompt to process
            
        Yields:
            String tokens as they are generated
        """
        pass
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        self.context.messages.append(AgentMessage(role=role, content=content))
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.context.messages = []
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent.
        
        Override in subclasses to customize behavior.
        """
        return f"You are {self.name}, {self.description}."
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"
