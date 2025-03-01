import pytest
from at_common_workflow.core.workflow import WorkflowBuilder
from at_common_workflow.core.constants import WorkflowEventType
from pydantic import BaseModel
import asyncio
import time
from typing import AsyncIterator

class AddInputModel(BaseModel):
    a: int
    b: int

class AddOutputModel(BaseModel):
    result: int

async def execute_add(input: AddInputModel) -> AddOutputModel:
    return AddOutputModel(result=input.a + input.b)

@pytest.mark.asyncio
async def test_task_builder_initialization():
    workflow = (WorkflowBuilder()
        .define_processing_task("add_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_func=execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("add_task_result", "result")
        .build()
    )

    # Assert that the workflow is not None
    assert workflow is not None

    # Assert that the task was added to the workflow
    assert len(workflow.nodes) == 1  # Assuming only one task is added

    # Assert that the task's name is correct
    task_node = workflow.nodes[0]
    assert task_node.task.name == "add_task"

    # Assert that the input model is set correctly
    assert task_node.task.input_model is AddInputModel

    # Assert that the output model is set correctly
    assert task_node.task.output_model is AddOutputModel

    # Assert that the constant arguments are mapped correctly
    assert task_node.argument_mappings["a"].value == 5
    assert task_node.argument_mappings["b"].value == 3

    # Assert that the result mapping is set correctly
    assert task_node.result_mapping.context_key == "add_task_result"

@pytest.mark.asyncio
async def test_task_builder_with_description():
    workflow = (WorkflowBuilder()
        .define_processing_task("add_task")
            .with_description("Adds two numbers")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result")
        .build()
    )
    
    assert workflow.nodes[0].task.description == "Adds two numbers"

@pytest.mark.asyncio
async def test_task_builder_with_context_arg():
    workflow = (WorkflowBuilder()
        .define_processing_task("first_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("first_result", "result")
        .define_processing_task("second_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_context_arg("a", "first_result")
            .with_constant_arg("b", 2)
        .add("final_result", "result")
        .build()
    )
    
    assert len(workflow.nodes) == 2
    second_task = workflow.nodes[1]
    assert second_task.argument_mappings["a"].value == "$first_result"
    assert second_task.argument_mappings["b"].value == 2

@pytest.mark.asyncio
async def test_task_builder_invalid_input_model():
    class InvalidModel:  # Not a Pydantic model
        pass
    
    with pytest.raises(TypeError, match="input_model must be a Pydantic BaseModel class"):
        (WorkflowBuilder()
            .define_processing_task("invalid_task")
                .with_input_model(InvalidModel)
        )

@pytest.mark.asyncio
async def test_task_builder_missing_required_components():
    # Missing input model
    with pytest.raises(ValueError, match="Input model must be defined"):
        (WorkflowBuilder()
            .define_processing_task("incomplete_task")
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_add)
                .with_constant_arg("a", 1)
                .with_constant_arg("b", 2)
            .add("result")
        )
    
    # Missing execute function
    with pytest.raises(ValueError, match="Execute function must be defined"):
        (WorkflowBuilder()
            .define_processing_task("incomplete_task")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_constant_arg("a", 1)
                .with_constant_arg("b", 2)
            .add("result")
        )

@pytest.mark.asyncio
async def test_task_builder_invalid_constant_arg():
    with pytest.raises(ValueError, match="Constant argument .* looks like a context reference"):
        (WorkflowBuilder()
            .define_processing_task("invalid_task")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_add)
                .with_constant_arg("a", "$invalid_ref")
        )

@pytest.mark.asyncio
async def test_multiple_tasks_workflow():
    # Create a more complex workflow with multiple tasks
    workflow = (WorkflowBuilder()
        .define_processing_task("task1")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result1", "result")
        .define_processing_task("task2")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_context_arg("a", "result1")
            .with_constant_arg("b", 2)
        .add("final_result", "result")
        .build()
    )
    
    assert len(workflow.nodes) == 2
    
    # Verify first task
    task1 = workflow.nodes[0]
    assert task1.task.name == "task1"
    assert task1.argument_mappings["a"].value == 5
    assert task1.argument_mappings["b"].value == 3
    assert task1.result_mapping.context_key == "result1"
    assert task1.result_mapping.result_path == "result"
    
    # Verify second task
    task2 = workflow.nodes[1]
    assert task2.task.name == "task2"
    assert task2.argument_mappings["a"].value == "$result1"
    assert task2.argument_mappings["b"].value == 2
    assert task2.result_mapping.context_key == "final_result"
    assert task2.result_mapping.result_path == "result"

@pytest.mark.asyncio
async def test_task_builder_invalid_output_model():
    class InvalidModel:  # Not a Pydantic model
        pass
    
    with pytest.raises(TypeError, match="output_model must be a Pydantic BaseModel class"):
        (WorkflowBuilder()
            .define_processing_task("invalid_task")
                .with_input_model(AddInputModel)
                .with_output_model(InvalidModel)
        )

@pytest.mark.asyncio
async def test_task_builder_chaining():
    # Test that all builder methods return self for proper chaining
    builder = WorkflowBuilder().define_processing_task("chain_task")
    
    # Test each method returns the builder instance
    assert builder.with_description("test") is builder
    assert builder.with_input_model(AddInputModel) is builder
    assert builder.with_output_model(AddOutputModel) is builder
    assert builder.with_execute_func(execute_add) is builder
    assert builder.with_constant_arg("a", 1) is builder
    assert builder.with_context_arg("b", "some_key") is builder

@pytest.mark.asyncio
async def test_task_builder_result_paths():
    # Create a more complex output model for testing result paths
    class ComplexOutputModel(BaseModel):
        value: int
        nested: dict
        items: list

    async def complex_execute(input: AddInputModel) -> ComplexOutputModel:
        return ComplexOutputModel(
            value=input.a + input.b,
            nested={"result": input.a * input.b},
            items=[input.a, input.b]
        )

    workflow = (WorkflowBuilder()
        .define_processing_task("complex_task")
            .with_input_model(AddInputModel)
            .with_output_model(ComplexOutputModel)
            .with_execute_func(complex_execute)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result1", "value")  # Store just the value field
        .define_processing_task("nested_task")
            .with_input_model(AddInputModel)
            .with_output_model(ComplexOutputModel)
            .with_execute_func(complex_execute)
            .with_constant_arg("a", 2)
            .with_constant_arg("b", 4)
        .add("result2", "nested.result")  # Store nested field
        .build()
    )
    
    assert len(workflow.nodes) == 2
    assert workflow.nodes[0].result_mapping.result_path == "value"
    assert workflow.nodes[1].result_mapping.result_path == "nested.result"

@pytest.mark.asyncio
async def test_task_builder_duplicate_task_names():
    workflow_builder = WorkflowBuilder()
    
    # Add first task
    workflow_builder.define_processing_task("same_name") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 1) \
        .with_constant_arg("b", 2) \
    .add("result1")
    
    # Add second task with same name
    workflow_builder.define_processing_task("same_name") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 3) \
        .with_constant_arg("b", 4) \
    .add("result2")
    
    # Build should succeed as duplicate names are allowed
    workflow = workflow_builder.build()
    assert len(workflow.nodes) == 2
    assert workflow.nodes[0].task.name == "same_name"
    assert workflow.nodes[1].task.name == "same_name"

class UserInputModel(BaseModel):
    user_id: str
    user_data: dict

class UserOutputModel(BaseModel):
    processed: bool
    data: dict

async def process_user(input: UserInputModel) -> UserOutputModel:
    return UserOutputModel(
        processed=True,
        data={"id": input.user_id, **input.user_data}
    )

@pytest.mark.asyncio
async def test_task_builder_context_arg_variations():
    """Test different ways of using with_context_arg"""
    
    # Build workflow with both single and dictionary context mappings
    workflow = (WorkflowBuilder()
        .define_processing_task("process_user")
            .with_input_model(UserInputModel)
            .with_output_model(UserOutputModel)
            .with_execute_func(process_user)
            # Test single value context mapping
            .with_context_arg("user_id", "user.id")
            # Test dictionary context mapping
            .with_context_arg("user_data", {
                "role": "user.role",
                "settings": "user.settings",
                "preferences": "user.prefs"
            })
        .add("result")
        .build()
    )

    # Verify argument mappings were created correctly
    process_task = workflow.nodes[0]
    
    # Check single value mapping
    assert process_task.argument_mappings["user_id"].value == "$user.id"
    
    # Check dictionary mapping
    user_data_mapping = process_task.argument_mappings["user_data"]
    assert user_data_mapping.dict_mapping == {
        "role": "$user.role",
        "settings": "$user.settings",
        "preferences": "$user.prefs"
    }
    
    # Test actual execution
    workflow.context.set("user.id", "123")
    workflow.context.set("user.role", "admin")
    workflow.context.set("user.settings", {"theme": "dark"})
    workflow.context.set("user.prefs", {"notifications": True})
    
    # Execute workflow
    async for _ in workflow.execute():
        pass
    
    # Verify results
    result = workflow.context.get("result")
    assert result.processed == True
    assert result.data["id"] == "123"
    assert result.data["role"] == "admin"
    assert result.data["settings"] == {"theme": "dark"}
    assert result.data["preferences"] == {"notifications": True}

@pytest.mark.asyncio
async def test_task_builder_context_arg_dollar_prefix():
    """Test that dollar prefix handling works correctly"""
    workflow = (WorkflowBuilder()
        .define_processing_task("process_user")
            .with_input_model(UserInputModel)
            .with_output_model(UserOutputModel)
            .with_execute_func(process_user)
            # Test with and without dollar prefix
            .with_context_arg("user_id", "$user.id")
            .with_context_arg("user_data", {
                "role": "$user.role",
                "settings": "user.settings"  # No dollar prefix
            })
        .add("result")
        .build()
    )

    process_task = workflow.nodes[0]
    
    # Both should have dollar prefix in final mapping
    assert process_task.argument_mappings["user_id"].value == "$user.id"
    assert process_task.argument_mappings["user_data"].dict_mapping == {
        "role": "$user.role",
        "settings": "$user.settings"
    }

@pytest.mark.asyncio
async def test_task_builder_context_arg_nested_paths():
    """Test that deeply nested context paths work correctly"""
    workflow = (WorkflowBuilder()
        .define_processing_task("process_user")
            .with_input_model(UserInputModel)
            .with_output_model(UserOutputModel)
            .with_execute_func(process_user)
            .with_context_arg("user_id", "users.current.id")
            .with_context_arg("user_data", {
                "role": "users.current.roles.primary",
                "settings": "users.current.preferences.settings"
            })
        .add("result")
        .build()
    )

    # Set up nested context
    workflow.context.set("users.current.id", "123")
    workflow.context.set("users.current.roles.primary", "admin")
    workflow.context.set("users.current.preferences.settings", {"theme": "dark"})
    
    # Execute workflow
    async for _ in workflow.execute():
        pass
    
    # Verify results
    result = workflow.context.get("result")
    assert result.processed == True
    assert result.data["id"] == "123"
    assert result.data["role"] == "admin"
    assert result.data["settings"] == {"theme": "dark"}

@pytest.mark.asyncio
async def test_workflow_execution_error_handling():
    """Test that errors during task execution are properly handled."""
    
    async def failing_execute(input: AddInputModel) -> AddOutputModel:
        raise ValueError("Simulated error")
    
    workflow = (WorkflowBuilder()
        .define_processing_task("failing_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(failing_execute)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result")
        .build()
    )
    
    # Execute workflow and expect an error
    with pytest.raises(RuntimeError):
        async for _ in workflow.execute():
            pass

@pytest.mark.asyncio
async def test_workflow_cyclic_dependencies():
    """Test that cyclic dependencies are detected."""
    
    workflow_builder = WorkflowBuilder()
    
    # Add first task
    workflow_builder.define_processing_task("task1") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 1) \
        .with_context_arg("b", "result2") \
        .add("result1")
    
    # Add second task with dependency on first task's result
    workflow_builder.define_processing_task("task2") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_context_arg("a", "result1") \
        .with_constant_arg("b", 2) \
        .add("result2")
    
    # Building should fail due to cyclic dependency
    with pytest.raises(ValueError, match="Cyclic dependencies detected"):
        workflow_builder.build()

@pytest.mark.asyncio
async def test_workflow_events():
    """Test that workflow events are emitted correctly."""
    
    workflow = (WorkflowBuilder()
        .define_processing_task("add_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result")
        .build()
    )
    
    events = []
    async for event in workflow.execute():
        events.append(event)
    
    # Verify events
    assert len(events) >= 3  # At least WORKFLOW_STARTED, TASK_STARTED, TASK_COMPLETED, WORKFLOW_COMPLETED
    assert events[0].type == WorkflowEventType.WORKFLOW_STARTED
    assert any(e.type == WorkflowEventType.TASK_STARTED and e.task_name == "add_task" for e in events)
    assert any(e.type == WorkflowEventType.TASK_COMPLETED and e.task_name == "add_task" for e in events)
    assert events[-1].type == WorkflowEventType.WORKFLOW_COMPLETED

@pytest.mark.asyncio
async def test_parallel_task_execution():
    """Test that independent tasks execute in parallel."""
    
    # Create a task that takes some time to complete
    async def slow_execute(input: AddInputModel) -> AddOutputModel:
        await asyncio.sleep(0.1)  # Simulate work
        return AddOutputModel(result=input.a + input.b)
    
    # Create a workflow with two independent tasks
    workflow = (WorkflowBuilder()
        .define_processing_task("task1")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(slow_execute)
            .with_constant_arg("a", 1)
            .with_constant_arg("b", 2)
        .add("result1")
        .define_processing_task("task2")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(slow_execute)
            .with_constant_arg("a", 3)
            .with_constant_arg("b", 4)
        .add("result2")
        .build()
    )
    
    # Execute and time it
    start_time = time.time()
    async for _ in workflow.execute():
        pass
    execution_time = time.time() - start_time
    
    # If tasks ran in parallel, execution time should be close to 0.1s
    # If they ran sequentially, it would be closer to 0.2s
    assert execution_time < 0.15  # Allow some margin for test overhead

class StreamingInputModel(BaseModel):
    count: int

class StreamingOutputModel(BaseModel):
    value: int

async def streaming_counter(input: StreamingInputModel) -> AsyncIterator[StreamingOutputModel]:
    """Example streaming task that yields numbers up to count."""
    for i in range(input.count):
        yield StreamingOutputModel(value=i)
        await asyncio.sleep(0.1)  # Simulate some processing time

@pytest.mark.asyncio
async def test_streaming_task():
    """Test that streaming tasks emit events correctly."""
    
    workflow = (WorkflowBuilder()
        .define_processing_task("counter")
            .with_input_model(StreamingInputModel)
            .with_output_model(StreamingOutputModel)
            .with_execute_func(streaming_counter)
            .with_constant_arg("count", 5)
        .add("final_count")
        .build()
    )
    
    events = []
    async for event in workflow.execute():
        events.append(event)
    
    # Verify events
    assert len(events) >= 7  # WORKFLOW_STARTED + TASK_STARTED + 5 STREAM_DATA + TASK_COMPLETED + WORKFLOW_COMPLETED
    assert events[0].type == WorkflowEventType.WORKFLOW_STARTED
    
    # Verify streaming events
    stream_events = [e for e in events if e.type == WorkflowEventType.TASK_STREAM_DATA]
    assert len(stream_events) == 5
    
    # Verify stream data values
    for i, event in enumerate(stream_events):
        assert event.task_name == "counter"
        assert event.stream_data.value == i
    
    assert events[-1].type == WorkflowEventType.WORKFLOW_COMPLETED