from typing import Set, AsyncIterator, List
import asyncio
import logging
from at_common_workflow.core.workflow.node import Node
from at_common_workflow.core.constants import TaskStatus, WorkflowEventType
from at_common_workflow.core.context import Context
from at_common_workflow.core.workflow.graph.dependency import DependencyManager
from .events import WorkflowEvent
from .progress import Progress

class WorkflowExecutor:
    """Handles the execution of tasks in a workflow."""
    
    def __init__(self, 
                 nodes: List[Node], 
                 context: Context, 
                 progress: Progress, 
                 dependency_manager: DependencyManager,
                 logger: logging.Logger):
        self.nodes = nodes
        self.context = context
        self.progress = progress
        self.dependency_manager = dependency_manager
        self.logger = logger
    
    def _get_ready_tasks(self, completed_tasks: Set[str]) -> Set[str]:
        """Get tasks whose dependencies are all satisfied and required context keys are available."""
        ready_tasks = set()
        for node in self.nodes:
            task_name = node.task.name
            if (task_name in completed_tasks or 
                self.progress.task_statuses.get(task_name, TaskStatus.PENDING) != TaskStatus.PENDING):
                continue

            dependencies = self.dependency_manager.get_dependencies(task_name)
            if all(dep in completed_tasks for dep in dependencies):
                # Check context availability
                all_context_available = True
                for arg_mapping in node.argument_mappings.values():
                    if arg_mapping.is_context_ref:
                        context_key = arg_mapping.value[1:]  # Remove $ prefix
                        if context_key not in self.context:
                            all_context_available = False
                            break
                if all_context_available:
                    ready_tasks.add(task_name)
        return ready_tasks
    
    async def _execute_task(self, task_name: str) -> AsyncIterator[WorkflowEvent]:
        """Execute a single task and update its status."""
        node = next(t for t in self.nodes if t.task.name == task_name)
        
        self.logger.info(f"Starting task: {task_name}")
        self.progress.update_task_status(task_name, TaskStatus.RUNNING)           
        try:
            args = {
                name: mapping.resolve(self.context)
                for name, mapping in node.argument_mappings.items()
            }
            
            self.logger.debug(f"Task {task_name} arguments resolved: {args}")
            result = await node.task(**args)
            
            # Handle streaming results
            if hasattr(result, '__aiter__'):
                async for stream_data in result:
                    yield WorkflowEvent(
                        WorkflowEventType.TASK_STREAM_DATA,
                        task_name=task_name,
                        stream_data=stream_data
                    )
                # Store the last stream item as the final result
                node.result_mapping.store(self.context, stream_data)
            else:
                # Handle regular non-streaming results
                node.result_mapping.store(self.context, result)
            
            self.logger.info(f"Task completed successfully: {task_name}")
            self.progress.update_task_status(task_name, TaskStatus.COMPLETED)
        except Exception as e:
            self.logger.error(f"Task failed: {task_name}", exc_info=True)
            self.progress.update_task_status(task_name, TaskStatus.FAILED)
            yield WorkflowEvent(WorkflowEventType.TASK_FAILED, task_name=task_name, error=e)
            raise
    
    async def execute(self) -> AsyncIterator[WorkflowEvent]:
        """
        Execute tasks in parallel when possible based on their dependencies.
        Yields workflow events during execution.
        """
        self.logger.info("Starting workflow execution")
        yield WorkflowEvent(WorkflowEventType.WORKFLOW_STARTED)
        
        try:
            completed_tasks: Set[str] = set()
            tasks_in_progress = set()
            
            while len(completed_tasks) < len(self.nodes):
                ready_tasks = self._get_ready_tasks(completed_tasks) - tasks_in_progress
                
                if not ready_tasks and not tasks_in_progress:
                    remaining = {t.task.name for t in self.nodes} - completed_tasks
                    msg = f"Unable to make progress. Tasks stuck: {remaining}"
                    self.logger.error(msg)
                    raise RuntimeError(msg)
                
                if ready_tasks:
                    self.logger.debug(f"Starting new tasks: {ready_tasks}")
                
                running_tasks = set()
                for task_name in ready_tasks:
                    # Create a coroutine that executes the task and collects events
                    async def execute_task_wrapper(task_name: str):
                        events = []
                        async for event in self._execute_task(task_name):
                            events.append(event)
                        return events
                    
                    running_tasks.add(asyncio.create_task(execute_task_wrapper(task_name)))
                    tasks_in_progress.add(task_name)
                    yield WorkflowEvent(WorkflowEventType.TASK_STARTED, task_name=task_name)
                
                if running_tasks:
                    done, _ = await asyncio.wait(running_tasks, return_when=asyncio.ALL_COMPLETED)
                    
                    for task in done:
                        try:
                            # Get collected events from the task
                            events = await task
                            for event in events:
                                yield event
                            
                            completed_task_name = next(
                                name for name in tasks_in_progress 
                                if self.progress.task_statuses[name] == TaskStatus.COMPLETED
                            )
                            completed_tasks.add(completed_task_name)
                            tasks_in_progress.remove(completed_task_name)
                            yield WorkflowEvent(WorkflowEventType.TASK_COMPLETED, task_name=completed_task_name)
                            self.logger.debug(f"Task completed and removed from in-progress: {completed_task_name}")
                        except Exception as e:
                            self.logger.error("Workflow execution failed", exc_info=True)
                            raise RuntimeError("Workflow execution failed") from e
            
            self.logger.info("Workflow execution completed successfully")
            yield WorkflowEvent(WorkflowEventType.WORKFLOW_COMPLETED)
            
        except Exception as e:
            self.logger.error("Workflow execution failed", exc_info=True)
            yield WorkflowEvent(WorkflowEventType.WORKFLOW_FAILED, error=e)
            raise