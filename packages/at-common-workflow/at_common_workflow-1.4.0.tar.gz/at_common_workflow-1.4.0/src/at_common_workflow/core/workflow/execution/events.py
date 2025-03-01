from dataclasses import dataclass
from typing import Optional, Any
from at_common_workflow.core.constants import WorkflowEventType

@dataclass
class WorkflowEvent:
    """Event emitted during workflow execution."""
    type: WorkflowEventType
    task_name: Optional[str] = None
    error: Optional[Exception] = None
    stream_data: Optional[Any] = None  # New field for streaming data