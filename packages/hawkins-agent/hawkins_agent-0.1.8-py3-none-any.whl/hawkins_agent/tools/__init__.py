"""
Hawkins Agent Tools
A collection of tools for use with Hawkins agents
"""

from .base import BaseTool
from .email import EmailTool
from .search import WebSearchTool
from .rag import RAGTool
from .summarize import SummarizationTool
from .code_interpreter import CodeInterpreterTool
from .weather import WeatherTool

# Dictionary of available tools for UI and configuration
available_tools = {
    "EmailTool": EmailTool,
    "WebSearchTool": WebSearchTool,
    "RAGTool": RAGTool,
    "SummarizationTool": SummarizationTool,
    "CodeInterpreterTool": CodeInterpreterTool,
    "WeatherTool": WeatherTool
}

__all__ = [
    "BaseTool",
    "EmailTool", 
    "WebSearchTool",
    "RAGTool",
    "SummarizationTool",
    "CodeInterpreterTool",
    "WeatherTool",
    "available_tools"
]