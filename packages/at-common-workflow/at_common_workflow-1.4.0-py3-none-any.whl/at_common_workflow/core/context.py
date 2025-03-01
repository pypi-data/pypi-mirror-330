from typing import Any, Dict
from threading import RLock

class Context:
    """
    A dictionary-like class that stores key-value pairs throughout workflow execution.
    
    Features:
    - Supports dot notation access (e.g., context.user.name)
    - Supports nested keys using dot notation in strings (e.g., "user.name")
    - Raises KeyError for missing or invalid paths
    """
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self._lock = RLock()  # Using RLock to allow recursive locking
    
    def __getattr__(self, key: str) -> Any:
        """Access context values using attribute notation."""
        with self._lock:
            return self.get(key)
    
    def __setattr__(self, key: str, value: Any) -> None:
        if key in ('_data', '_lock'):
            super().__setattr__(key, value)
        else:
            with self._lock:
                self.set(key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value using dot notation for nested access.
        
        Args:
            key: Key to look up, can use dot notation for nested access
            default: Value to return if key is not found. If not provided, raises KeyError
        
        Raises:
            KeyError: If the key is not found and no default value is provided
        """
        with self._lock:
            parts = key.split('.')
            current = self._data
            for part in parts:
                if isinstance(current, dict):
                    if part not in current:
                        if default is None:
                            raise KeyError(f"Key '{key}' not found in context")
                        return default
                    current = current[part]
                else:
                    if default is None:
                        raise KeyError(f"Cannot access '{part}' in '{key}': parent is not a dict")
                    return default
            return current
    
    def set(self, key: str, value: Any) -> None:
        """Set value using dot notation for nested access."""
        with self._lock:
            parts = key.split('.')
            current = self._data
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator for checking key existence."""
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def __repr__(self) -> str:
        """Provide readable string representation."""
        return f"Context({self._data})"