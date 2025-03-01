from typing import Dict, Set, List
from at_common_workflow.core.workflow.node import Node

class DependencyManager:
    """Manages task dependencies in a workflow."""
    
    def __init__(self):
        self._task_dependencies: Dict[str, Set[str]] = {}
        self._reverse_dependencies: Dict[str, Set[str]] = {}
        
    def initialize(self, nodes: List[Node]) -> None:
        """Initialize dependency dictionaries for all tasks."""
        self._task_dependencies.clear()
        self._reverse_dependencies.clear()
        for node in nodes:
            task_name = node.task.name
            self._task_dependencies[task_name] = set()
            self._reverse_dependencies[task_name] = set()
    
    def add_dependency(self, dependent: str, provider: str) -> None:
        """Add a dependency between tasks."""
        self._task_dependencies[dependent].add(provider)
        self._reverse_dependencies[provider].add(dependent)
    
    def get_dependencies(self, task_name: str) -> Set[str]:
        """Get dependencies for a task."""
        return self._task_dependencies.get(task_name, set())
    
    def get_dependents(self, task_name: str) -> Set[str]:
        """Get tasks that depend on this task."""
        return self._reverse_dependencies.get(task_name, set())
    
    def has_cycle(self) -> bool:
        """Check for cycles in the dependency graph."""
        visited = set()
        temp_visited = set()
        
        def _has_cycle(task_name: str) -> bool:
            if task_name in temp_visited:
                return True
            if task_name in visited:
                return False
            
            temp_visited.add(task_name)
            
            for dep in self._task_dependencies[task_name]:
                if _has_cycle(dep):
                    return True
                    
            temp_visited.remove(task_name)
            visited.add(task_name)
            return False
        
        for task_name in self._task_dependencies:
            if _has_cycle(task_name):
                return True
        
        return False
    
    def find_cycle_task(self) -> str:
        """Find a task that is part of a cycle."""
        visited = set()
        temp_visited = set()
        cycle_task = None
        
        def _find_cycle(task_name: str) -> bool:
            nonlocal cycle_task
            if task_name in temp_visited:
                cycle_task = task_name
                return True
            if task_name in visited:
                return False
            
            temp_visited.add(task_name)
            
            for dep in self._task_dependencies[task_name]:
                if _find_cycle(dep):
                    return True
                    
            temp_visited.remove(task_name)
            visited.add(task_name)
            return False
        
        for task_name in self._task_dependencies:
            if _find_cycle(task_name):
                return cycle_task
        
        return None