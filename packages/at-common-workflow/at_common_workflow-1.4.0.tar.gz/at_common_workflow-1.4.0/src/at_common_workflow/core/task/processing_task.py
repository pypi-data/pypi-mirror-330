from typing import Type, Any, Callable, AsyncIterator, Union
from .base import BaseTask, InputType, OutputType
from .validation import validate_task_configuration

class ProcessingTask(BaseTask[InputType, OutputType]):
    """
    Represents a processing task in a workflow with typed input and output.
    
    A processing task:
    - Accepts input conforming to a Pydantic model
    - Processes that input according to business logic
    - Produces output conforming to a Pydantic model
    - Can optionally stream data during processing
    """
    
    def __init__(
        self, 
        name: str,
        description: str | None,
        input_model: Type[InputType],
        output_model: Type[OutputType],
        execute_func: Callable[[InputType], Union[OutputType, AsyncIterator[OutputType]]]
    ):
        """
        Initialize a processing task with its configuration.
        
        Args:
            name: Unique task name
            description: Optional task description
            input_model: Pydantic model class for input validation
            output_model: Pydantic model class for output validation
            execute_func: Function that executes the task logic. Can return either:
                        - A single output value
                        - An async iterator for streaming output
        """
        super().__init__(name, description)
        self.input_model = input_model
        self.output_model = output_model
        self.execute_func = execute_func
        self._validate()
        
    def _validate(self) -> None:
        """Validate that task configuration is properly defined."""
        validate_task_configuration(
            self.name,
            self.input_model,
            self.output_model,
            self.execute_func
        )
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f"{self.__class__.__name__}(name={self.name!r})(description={self.description!r}) {self.input_model.__name__} -> {self.output_model.__name__}"
    
    def _validate_input(self, **kwargs) -> InputType:
        """
        Validate input arguments against input_model.
        
        Args:
            **kwargs: Input arguments
            
        Returns:
            Validated input model instance
        """
        return self.input_model(**kwargs)
    
    def _validate_output(self, output: Any) -> OutputType:
        """
        Validate output against output_model.
        
        Args:
            output: Task output
            
        Returns:
            Validated output model instance
        """
        if isinstance(output, self.output_model):
            return output
        return self.output_model(**output)
    
    async def __call__(self, **kwargs) -> Union[OutputType, AsyncIterator[OutputType]]:
        """
        Allow tasks to be called directly for testing/debugging.
        Validates both input and output.
        
        Args:
            **kwargs: Input arguments
            
        Returns:
            Either a single validated output model instance or an async iterator of validated outputs
        """
        input = self._validate_input(**kwargs)
        result = self.execute_func(input)
        
        # Check if the result is an async generator
        if hasattr(result, '__aiter__'):
            async def validate_stream():
                async for item in result:
                    yield self._validate_output(item)
            return validate_stream()
        
        # If not an async generator, it must be a regular coroutine
        result = await result
        return self._validate_output(result)