from typing import Any, Optional, Union, Dict, List
from pydantic import BaseModel

from at_common_workflow.core.context import Context

class BaseMapping:
    """Base class for all mapping types."""
    
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class ArgumentMapping(BaseMapping):
    """Maps context values or constants to task arguments."""
    
    def __init__(self, value: Union[str, Any], dict_mapping: Optional[Dict[str, str]] = None):
        self.value = value
        self.dict_mapping = dict_mapping
        self.is_context_ref = isinstance(value, str) and value.startswith("$")
        self.is_dict_mapping = dict_mapping is not None
    
    def get_context_refs(self) -> List[str]:
        """Get all context references used in this mapping."""
        refs = []
        if self.is_context_ref:
            refs.append(self.value[1:])  # Remove $ prefix
        if self.is_dict_mapping:
            for value in self.dict_mapping.values():
                if value.startswith('$'):
                    refs.append(value[1:])
        return refs

    def resolve(self, context: Context) -> Any:
        """Resolve the mapping value from context if it's a reference."""
        if self.is_dict_mapping:
            return {
                key: context.get(context_key.lstrip('$'))
                for key, context_key in self.dict_mapping.items()
            }
        if self.is_context_ref:
            return context.get(self.value[1:])
        return self.value

class ResultMapping(BaseMapping):
    """Maps task results to context keys."""
    
    def __init__(self, context_key: str, result_path: Optional[str] = None):
        self.context_key = context_key
        self.result_path = result_path
    
    def store(self, context: Context, result: BaseModel) -> None:
        """Store the task result in the context."""
        value = getattr(result, self.result_path) if self.result_path else result
        context.set(self.context_key, value)