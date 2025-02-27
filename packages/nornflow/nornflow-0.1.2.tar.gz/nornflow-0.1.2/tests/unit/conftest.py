import pytest

from nornflow.nornflow import NornFlow
from nornflow.settings import NornFlowSettings
from nornflow.workflow import Workflow


@pytest.fixture
def valid_workflow_dict(request):
    """Get a valid workflow dictionary with a unique task name."""
    return {
        "workflow": {
            "name": f"Test Workflow {request.function.__name__}",
            "description": "A test workflow",
            "inventory_filters": {"hosts": ["host1", "host2"], "groups": ["group1"]},
            "tasks": [{"name": f"{request.function.__name__}_task", "args": {"arg1": ["value1", "value2"]}}],
        }
    }


@pytest.fixture
def invalid_workflow_dict():
    """Get an invalid workflow dictionary (missing tasks)."""
    return {
        "workflow": {
            "name": "Test Workflow",
            "description": "A test workflow",
            "inventory_filters": {"hosts": [], "groups": []},
        }
    }


@pytest.fixture
def valid_workflow_file(tmp_path, request):
    """Create a temporary valid workflow file with a unique task name."""
    workflow_file = tmp_path / "valid_workflow.yaml"
    workflow_file.write_text(
        f"""
workflow:
  name: Test Workflow {request.function.__name__}
  description: A test workflow
  inventory_filters:
    hosts: []
    groups: []
  tasks:
    - name: {request.function.__name__}_task
      args:
        arg1: value1
"""
    )
    return workflow_file


@pytest.fixture
def invalid_workflow_file(tmp_path):
    """Create a temporary invalid workflow file."""
    workflow_file = tmp_path / "invalid_workflow.yaml"
    workflow_file.write_text(
        """
workflow:
  name: Test Workflow
  description: A test workflow
  inventory_filters:
    hosts: []
    groups: []
"""
    )
    return workflow_file


@pytest.fixture
def valid_workflow(valid_workflow_dict):
    """Create a valid workflow object."""
    return Workflow(valid_workflow_dict)


@pytest.fixture
def task_content():
    """Return the content of a basic Nornir task."""
    return """
from nornir.core.task import Task, Result

def hello_world(task: Task) -> Result:
    \"\"\"Say hello world\"\"\"
    return Result(host=task.host, result="Hello World!")
"""


@pytest.fixture
def basic_settings(tmp_path, task_content):
    """Create basic settings with a tasks directory containing one task."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    (tasks_dir / "task1.py").write_text(task_content)
    return NornFlowSettings(local_tasks_dirs=[str(tasks_dir)])


@pytest.fixture
def basic_nornflow(basic_settings):
    """Create a basic NornFlow instance."""
    return NornFlow(nornflow_settings=basic_settings)
