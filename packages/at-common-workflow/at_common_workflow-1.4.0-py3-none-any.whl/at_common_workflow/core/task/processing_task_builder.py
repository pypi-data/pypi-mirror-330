from typing import Callable, Any, Dict, Optional, TYPE_CHECKING, Type, Union
from pydantic import BaseModel
from at_common_workflow.utils.mappings import ArgumentMapping, ResultMapping
from .processing_task import ProcessingTask

if TYPE_CHECKING:
    from at_common_workflow.core.workflow import WorkflowBuilder

class ProcessingTaskBuilder:
    """
    Builder for creating and configuring tasks.
    """
    
    def __init__(self, wb: 'WorkflowBuilder', name: str) -> None:
        self._wb = wb
        self._name = name
        self._description: Optional[str] = None
        self._input_model: Optional[Type[BaseModel]] = None
        self._output_model: Optional[Type[BaseModel]] = None
        self._execute_func: Optional[Callable] = None
        
        self._argument_mappings: Dict[str, ArgumentMapping] = {}
        self._result_mapping: ResultMapping = None
    
    def with_description(self, description: str) -> 'ProcessingTaskBuilder':
        """Add a description to the task."""
        self._description = description
        return self

    def with_input_model(self, input_model: Type[BaseModel]) -> 'ProcessingTaskBuilder':
        """
        Add an input model class to the task.
        
        Args:
            input_model: A Pydantic BaseModel class defining the input parameters
            
        Returns:
            ProcessingTaskBuilder: The builder instance for method chaining
        """
        if not (isinstance(input_model, type) and issubclass(input_model, BaseModel)):
            raise TypeError("input_model must be a Pydantic BaseModel class")
        self._input_model = input_model
        return self
        
    def with_output_model(self, output_model: Type[BaseModel]) -> 'ProcessingTaskBuilder':
        """
        Add an output model class to the task.
        
        Args:
            output_model: A Pydantic BaseModel class defining the task's output
            
        Returns:
            TaskBuilder: The builder instance for method chaining
        """
        if not (isinstance(output_model, type) and issubclass(output_model, BaseModel)):
            raise TypeError("output_model must be a Pydantic BaseModel class")
        self._output_model = output_model
        return self
        
    def with_execute_func(self, execute_func: Callable) -> 'ProcessingTaskBuilder':
        """Set the execution function for the task."""
        self._execute_func = execute_func
        return self

    def with_constant_arg(self, name: str, value: Any) -> 'ProcessingTaskBuilder':
        """
        Add a constant value argument to the task.
        
        Args:
            name: Name of the argument
            value: Constant value to use
            
        Returns:
            TaskBuilder: The builder instance for method chaining
            
        Raises:
            ValueError: If the value looks like a context reference
        """
        # Prevent accidental context references
        if isinstance(value, str) and value.startswith('$'):
            raise ValueError(f"Constant argument '{name}' looks like a context reference: {value}")
        
        # Create argument mapping directly with the value
        self._argument_mappings[name] = ArgumentMapping(value=value)
        return self
    
    def with_context_arg(self, name: str, context_key: Union[str, Dict[str, str]]) -> 'ProcessingTaskBuilder':
        """
        Map an argument to one or more context values.
        
        Args:
            name: Name of the argument
            context_key: Either:
                - A string for direct context mapping (e.g., "user.id")
                - A dictionary mapping keys to context paths (e.g., {"id": "user.id", "role": "user.role"})
                
        Returns:
            TaskBuilder: The builder instance for method chaining
            
        Examples:
            # Single value mapping
            builder.with_context_arg("user_id", "user.id")
            
            # Dictionary mapping
            builder.with_context_arg("user_data", {
                "id": "user.id",
                "role": "user.role",
                "settings": "user.settings"
            })
        """
        if isinstance(context_key, dict):
            # Dictionary mapping case
            formatted_mapping = {
                key: f"${value}" if not value.startswith('$') else value
                for key, value in context_key.items()
            }
            self._argument_mappings[name] = ArgumentMapping(value=None, dict_mapping=formatted_mapping)
        else:
            # Single value case
            self._argument_mappings[name] = ArgumentMapping(value=f"${context_key}" if not context_key.startswith('$') else context_key)
        
        return self
    
    def add(self, context_key: str, result_path: Optional[str] = None) -> 'WorkflowBuilder':
        """
        Configure where to store the task result and add task to workflow.
        This finalizes the task configuration.
        """
        self._result_mapping = ResultMapping(context_key, result_path)

        # Validate required components first
        if not self._input_model:
            raise ValueError("Input model must be defined")
        if not self._output_model:
            raise ValueError("Output model must be defined")
        if not self._execute_func:
            raise ValueError("Execute function must be defined")
        
        # Create a ProcessingTask instead of Task
        task = ProcessingTask(
            name=self._name, 
            description=self._description, 
            input_model=self._input_model, 
            output_model=self._output_model,
            execute_func=self._execute_func
        )

        # Add task to workflow
        self._wb.workflow.add_task(
            task=task,
            argument_mappings=self._argument_mappings,
            result_mapping=self._result_mapping
        )
        return self._wb