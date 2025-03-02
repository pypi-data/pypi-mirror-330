"""
LocalLab - A lightweight AI inference server
"""

__version__ = "0.2.2" 

from typing import Dict, Any, Optional

# Export commonly used components
from .config import MODEL_REGISTRY, can_run_model
from .server import start_server

__all__ = ["start_server", "MODEL_REGISTRY", "can_run_model"]
