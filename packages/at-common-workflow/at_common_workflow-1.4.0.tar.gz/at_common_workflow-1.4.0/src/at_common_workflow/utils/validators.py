from typing import Any, Dict, TYPE_CHECKING
from ..core.exceptions import TaskValidationError, WorkflowValidationError
if TYPE_CHECKING:
    from ..core.workflow import Workflow
    from ..core.task import Task

def validate_workflow(workflow: 'Workflow') -> None:
    """Validate workflow configuration and dependencies"""
    try:
        workflow._build_dependency_graph()
    except Exception as e:
        raise WorkflowValidationError(f"Workflow validation failed: {str(e)}")

def validate_task(task: 'Task', input: Dict[str, Any]) -> None:
    """Validate task input data against its schema"""
    try:
        task.input_model(**input)
    except Exception as e:
        raise TaskValidationError(f"Task '{task.name}' validation failed: {str(e)}")