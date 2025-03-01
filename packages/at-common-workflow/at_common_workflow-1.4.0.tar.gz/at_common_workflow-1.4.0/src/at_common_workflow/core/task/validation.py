from typing import Type, Callable
from inspect import signature
from pydantic import BaseModel
from typing import AsyncIterator
from collections.abc import AsyncIterator as AsyncIteratorABC

def validate_task_configuration(
    name: str,
    input_model: Type,
    output_model: Type,
    execute_func: Callable
) -> None:
    """
    Validate task configuration parameters.
    
    Args:
        name: Task name
        input_model: Input model class
        output_model: Output model class
        execute_func: Task execution function
        
    Raises:
        TypeError: If any parameter has an invalid type
        ValueError: If any parameter has an invalid value
    """
    if not isinstance(name, str):
        raise TypeError("Task name must be a string")
    if not name.strip():
        raise ValueError("Task name cannot be empty")
    
    if not (isinstance(input_model, type) and issubclass(input_model, BaseModel)):
        raise TypeError(f"input_model must be a Pydantic model class")
    if not (isinstance(output_model, type) and issubclass(output_model, BaseModel)):
        raise TypeError(f"output_model must be a Pydantic model class")
    if not callable(execute_func):
        raise TypeError("execute_func must be callable")
    
    sig = signature(execute_func)
    if len(sig.parameters) != 1 or list(sig.parameters)[0] != 'input':
        raise TypeError("execute_func must take exactly one parameter named 'input'")

    # Check return type annotation
    return_type = sig.return_annotation
    return_type_str = str(return_type)

    # Check if it's a direct output model
    if return_type == output_model:
        return

    # Check if it's an AsyncIterator of output model
    if (hasattr(return_type, "__origin__") and 
        (return_type.__origin__ is AsyncIterator or return_type.__origin__ is AsyncIteratorABC) and
        len(return_type.__args__) == 1 and 
        return_type.__args__[0] == output_model):
        return

    # If we get here, the return type is invalid
    raise TypeError(f"execute_func must return either {output_model.__name__} or AsyncIterator[{output_model.__name__}]") 