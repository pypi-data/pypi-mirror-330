# Taskit - Task Management and Execution Framework

Taskit is a lightweight task management and execution framework designed to handle asynchronous tasks using Redis. It provides a simple way to publish tasks to specific channels and execute them in a concurrent manner using a pool of worker threads.

## Overview

Taskit's core components include:

- **Publishing tasks**: Using `publish`, tasks can be published to specific channels with relevant data and expiration time.
- **Task execution**: Tasks are executed concurrently by workers of a `TaskEngine`, which listens to specific channels for incoming tasks.
- **Redis-based queuing**: Task states such as pending, running, and error are maintained using Redis sets.

The framework is designed to work efficiently in environments where tasks need to be distributed and processed asynchronously.

## Usage

### Publishing a Task

The `taskit.publish` function is used to publish a task to a specified channel with the necessary data.

- **channel**: The channel to which the task will be published. It determines the workers that will pick up the task for execution.
- **function**: A string that provides the path to the function to be executed, e.g., `'my_module.my_function'`.
- **data**: A dictionary containing the task-specific data.
- **expires**: The time in seconds for the task data to expire from Redis. Defaults to 1800 seconds (30 minutes).

**Example**:

```python
import taskit

# Define custom the task data
task_data = {
    "model_id": 21,
    "example": {
        "key1": "value1",
        "key2": "value2"
    }
}

# Publish the task to a specific channel
taskit.publish_task('channel1', 'myapp.tasks.process_data', task_data)
```

### Task Execution

To execute tasks, you need to set up a `TaskEngine` and start it.

**Creating a TaskEngine**:

Create an instance of the `TaskEngine`, specifying the channels to listen to, the maximum number of parallel workers, and task expiration time.

**Syntax**:

```python
class TaskEngine:
    def __init__(self, channels, max_workers=5, task_expiration=3600):
        ...
```

- **channels**: A list of channels to listen to for tasks.
- **max_workers**: Maximum number of worker threads. Defaults to 5.
- **task_expiration**: Task expiration time in seconds. Defaults to 3600 seconds (1 hour).

**Example**:

```python
from django_jestit.taskit.runner import TaskEngine

# Initialize TaskEngine with desired configuration
engine = TaskEngine(channels=['channel1'], max_workers=10, task_expiration=3600)

# Start listening for tasks
engine.start_listening()
```

### Task function definition

Task functions should be defined in your application and include handling for the argument data passed via the `task_data` object. Ensure the function paths are provided during task publishing.

```python
# myapp/tasks.py

def process_data(task_data):
    # Extract arguments and keyword arguments
    args = task_data.get('args', [])
    kwargs = task_data.get('kwargs', {})

    # Process the data
    print("Processing data:", args, kwargs)
```

### Retrieving Task Status

While the `TaskEngine` maintains the state of tasks, you might want to check the status of tasks.

You can directly access it in the `TaskEngine`:

```python
engine.get_status()
```

This will provide a dictionary with lists of `pending_tasks`, `running_tasks`, and `error_tasks`.

## Notes

- The task function must be properly referenced by its full import path.
- Redis must be running and accessible from your application, and the Redis connection information should match your server setup.
- Handle exceptions in your task functions to prevent task fails from stopping the worker.

This framework can be extended or modified to suit specific asynchronous task processing needs in Python applications, taking advantage of Redis's capabilities.
