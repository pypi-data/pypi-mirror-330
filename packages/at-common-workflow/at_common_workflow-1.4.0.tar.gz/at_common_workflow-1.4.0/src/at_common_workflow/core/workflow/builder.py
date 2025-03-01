import logging
from pathlib import Path
from typing import Optional
from at_common_workflow.core.task import ProcessingTaskBuilder
from at_common_workflow.utils.logging import setup_logging
from .base import Workflow

class WorkflowBuilder:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.workflow = Workflow(logger=logger)
    
    def define_processing_task(self, name: str) -> 'ProcessingTaskBuilder':
        """Add a task to the workflow and return a ProcessingTaskBuilder for configuring it."""
        return ProcessingTaskBuilder(self, name=name)

    def build(self) -> Workflow:
        """
        Build and return the workflow.
        
        Returns:
            Workflow: The built and validated workflow
        
        Raises:
            WorkflowValidationError: If the workflow has validation errors
        """
        # Validate the workflow before returning it
        self.workflow._build_dependency_graph()
        return self.workflow

    @classmethod
    def with_logging(cls, 
        level: int = logging.INFO,
        log_file: Optional[Path] = None,
        format_string: Optional[str] = None
    ) -> 'WorkflowBuilder':
        """
        Create a WorkflowBuilder with configured logging.
        
        Args:
            level: Logging level
            log_file: Optional path to log file
            format_string: Optional custom format string for log messages
            
        Returns:
            WorkflowBuilder: Configured builder instance
        """
        logger = setup_logging(level, log_file, format_string)
        return cls(logger=logger)