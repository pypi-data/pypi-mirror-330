class WorkflowError(Exception):
    """Base exception for workflow-related errors"""
    pass

class TaskValidationError(WorkflowError):
    """Raised when task validation fails"""
    pass

class WorkflowValidationError(WorkflowError):
    """Raised when workflow validation fails"""
    pass