from typing import Generic, TypeVar
from pydantic import BaseModel

InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel) 

class BaseTask(Generic[InputType, OutputType]):
    """
    Base class for all task types in a workflow.
    
    A task:
    - Has a unique name
    - Has a description
    - Has specific validation logic
    """
    
    def __init__(
        self, 
        name: str, 
        description: str | None
    ):
        """
        Initialize a task with its basic configuration.
        
        Args:
            name: Unique task name
            description: Optional task description
        """
        self.name = name
        self.description = description
        
    def _validate(self) -> None:
        """
        Validate that task configuration is properly defined.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _validate method")
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f"{self.__class__.__name__}(name={self.name!r})(description={self.description!r})"