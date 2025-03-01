# At Common Workflow

## Description
At Common Workflow is a workflow management system that allows users to define and execute tasks in a directed acyclic graph (DAG) structure. It supports parallel execution and provides a context manager for managing task inputs and outputs.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd at-common-workflow
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
There are two ways to define tasks: using class inheritance or using the builder pattern.

### Class-based Approach
```python
from at_common_workflow.core.task import Task
from pydantic import BaseModel

class AddInputModel(BaseModel):
    a: int
    b: int

class AddOutputModel(BaseModel):
    result: int

class AddTask(Task[AddInputModel, AddOutputModel]):
    input_model = AddInputModel
    output_model = AddOutputModel
    
    async def _execute(self, input: AddInputModel) -> AddOutputModel:
        return AddOutputModel(result=input.a + input.b)

# Run workflow
workflow = Workflow()
task = AddTask("add_numbers")
workflow.add_task(task, argument_mappings={"a": 5, "b": 3}, result_mapping="result")
context = await workflow.execute()
print(context.get("result").result)  # Output: 8
```

### Builder Pattern Approach
```python
from at_common_workflow.builders import WorkflowBuilder

# Create and execute workflow
workflow = (WorkflowBuilder()
    .define_processing_task("add_numbers")
        .with_input_model(AddInputModel)
        .with_output_model(AddOutputModel)
        .with_execute_func(execute_add)
        .with_constant_arg("a", 5)
        .with_constant_arg("b", 3)
    .add("result")
    .build())

context = await workflow.execute()
print(context.get("result").result)  # Output: 8
```

## Logging Configuration

The workflow system supports comprehensive logging. Here's how to configure it:
```python
from at_common_workflow.builders import WorkflowBuilder
import logging
from pathlib import Path

# Configure workflow with logging
workflow_builder = WorkflowBuilder.with_logging(
    level=logging.DEBUG,
    log_file=Path("workflow.log"),
    format_string="[%(asctime)s] %(levelname)s: %(message)s"
)

# Build and execute workflow with logging
workflow = workflow_builder
    .define_processing_task("add_numbers")
        .with_input_model(AddInputModel)
        .with_output_model(AddOutputModel)
        .with_execute_func(execute_add)
        .with_constant_arg("a", 5)
        .with_constant_arg("b", 3)
    .add("result")
    .build()

# Execute workflow - all steps will be logged
context = await workflow.execute()



## Testing
To run the tests, use the following command:
```bash
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add.

## License
This project is licensed under the [MIT License](LICENSE).
