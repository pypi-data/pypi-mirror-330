from typing import Dict, Set
from at_common_workflow.core.task import ProcessingTask
from at_common_workflow.utils import ArgumentMapping, ResultMapping
from at_common_workflow.core.exceptions import TaskValidationError

class Node:
    """Represents a task node in the workflow graph."""
    
    def __init__(
        self,
        task: ProcessingTask,
        argument_mappings: Dict[str, ArgumentMapping],
        result_mapping: ResultMapping
    ) -> None:
        self._validate_arguments(task, argument_mappings)
        self.task = task
        self.argument_mappings = argument_mappings
        self.result_mapping = result_mapping
        self.dependencies: Set[str] = set()
    
    @staticmethod
    def _validate_arguments(task: ProcessingTask, argument_mappings: Dict[str, ArgumentMapping]) -> None:
        required_fields = {
            field_name for field_name, field in 
            task.input_model.model_fields.items()
            if field.is_required
        }
        missing_args = required_fields - argument_mappings.keys()
        if missing_args:
            raise TaskValidationError(
                f"Missing required arguments for task {task.name}: {missing_args}"
            )