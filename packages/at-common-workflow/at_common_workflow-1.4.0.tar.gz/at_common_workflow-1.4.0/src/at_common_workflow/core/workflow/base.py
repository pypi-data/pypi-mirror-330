from typing import List, Dict, Optional, AsyncIterator
import logging
from at_common_workflow.core.context import Context
from at_common_workflow.core.task import ProcessingTask
from at_common_workflow.utils import ArgumentMapping, ResultMapping
from at_common_workflow.utils.logging import setup_logging
from .node import Node
from .execution.progress import Progress
from .graph.dependency import DependencyManager
from .execution.executor import WorkflowExecutor
from .execution.events import WorkflowEvent
from at_common_workflow.core.constants import WorkflowEventType

class Workflow:
    """Orchestrates the execution of tasks in a directed acyclic graph with parallel execution support."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.nodes: List[Node] = []
        self.context = Context()
        self.progress = Progress()
        self.dependency_manager = DependencyManager()
        self.logger = logger or setup_logging()
    
    def add_task(
        self,
        task: ProcessingTask,
        argument_mappings: Dict[str, ArgumentMapping],
        result_mapping: ResultMapping
    ) -> None:
        """
        Add a task to the workflow with its argument mappings and result mapping.
        
        Args:
            task: The task to add
            argument_mappings: Dictionary mapping argument names to either:
                         - Context references (strings starting with $)
                         - Constant values
            result_mapping: Either:
                          - A string for the context key to store the entire result
                          - A tuple of (context_key, result_path) to store a specific field
        """           
        node = Node(task, argument_mappings, result_mapping)
        self.nodes.append(node)
    
    def _build_dependency_graph(self) -> None:
        """Build the dependency graph based on context references."""
        context_providers = {}
        referenced_keys = set()

        # First pass: collect all context providers and referenced keys
        for node in self.nodes:
            # Track providers
            context_key = node.result_mapping.context_key
            if context_key in context_providers:
                raise ValueError(
                    f"Multiple tasks trying to write to context key '{context_key}'"
                )
            context_providers[context_key] = node.task.name

            # Track references from both direct and dictionary mappings
            for arg_mapping in node.argument_mappings.values():
                referenced_keys.update(arg_mapping.get_context_refs())

        # Check for references to future task results
        for key in referenced_keys:
            if key in context_providers:
                continue
            # If the key is in the format "resultX" where X is a number, it's likely a reference to a future task
            if key.startswith("result"):
                raise ValueError(f"References undefined context key '{key}'")

        # Initialize dependency manager
        self.dependency_manager.initialize(self.nodes)

        # Second pass: build dependencies based on context references
        for node in self.nodes:
            task_name = node.task.name

            # Check context references in arguments
            for _, arg_mapping in node.argument_mappings.items():
                for context_key in arg_mapping.get_context_refs():
                    if context_key in context_providers:
                        provider_task = context_providers[context_key]
                        self.dependency_manager.add_dependency(task_name, provider_task)

        # Check for cycles in the dependency graph
        if self.dependency_manager.has_cycle():
            cycle_task = self.dependency_manager.find_cycle_task()
            raise ValueError(f"Cyclic dependencies detected in workflow: task '{cycle_task}' is part of a cycle")

    async def execute(self) -> AsyncIterator[WorkflowEvent]:
        """
        Execute tasks in parallel when possible based on their dependencies.
        Yields workflow events during execution.
        """
        try:
            self._build_dependency_graph()
            self.logger.debug("Dependency graph built successfully")
            
            executor = WorkflowExecutor(
                nodes=self.nodes,
                context=self.context,
                progress=self.progress,
                dependency_manager=self.dependency_manager,
                logger=self.logger
            )
            
            async for event in executor.execute():
                yield event
                
        except Exception as e:
            self.logger.error("Workflow execution failed", exc_info=True)
            yield WorkflowEvent(WorkflowEventType.WORKFLOW_FAILED, error=e)
            raise