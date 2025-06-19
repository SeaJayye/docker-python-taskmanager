# tests/test_core.py

import os
import json
import pytest
from task_manager import core, storage

TEST_FILE = "test_tasks.json"

# Fixture to isolate test data
@pytest.fixture(autouse=True)
def mock_storage(monkeypatch):
    monkeypatch.setattr(storage, "TASKS_FILE", TEST_FILE)
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

# P2P tests for task manager core functionality
def test_add_task():
    task = core.add_task("Write unit tests")
    assert task["title"] == "Write unit tests"
    assert task["done"] is False

def test_list_tasks():
    core.add_task("Task 1")
    core.add_task("Task 2")
    tasks = core.list_tasks()
    assert len(tasks) == 2

def test_complete_task():
    core.add_task("Finish homework")
    task = core.complete_task(0)
    assert task["done"] is True

def test_remove_task():
    core.add_task("Wash dishes")
    removed = core.remove_task(0)
    assert removed["title"] == "Wash dishes"

# Edge case tests and error handling
def test_remove_invalid_index():
    with pytest.raises(IndexError):
        core.remove_task(0)

def test_complete_invalid_index():
    with pytest.raises(IndexError):
        core.complete_task(0)

# Broader integration tests
def test_add_complete_and_list():
    # Add tasks
    core.add_task("Task A")
    core.add_task("Task B")
    core.add_task("Task C")
    
    # Complete second task
    core.complete_task(1)
    
    # List tasks and check states
    tasks = core.list_tasks()
    assert len(tasks) == 3
    assert tasks[0]["done"] is False
    assert tasks[1]["done"] is True    # Completed task
    assert tasks[2]["done"] is False

def test_remove_task_and_check_order():
    core.add_task("First Task")
    core.add_task("Second Task")
    core.add_task("Third Task")
    
    removed = core.remove_task(1)  # Remove "Second Task"
    assert removed["title"] == "Second Task"
    
    tasks = core.list_tasks()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "First Task"
    assert tasks[1]["title"] == "Third Task"

def test_complete_then_remove():
    core.add_task("Clean room")
    core.add_task("Do laundry")
    
    core.complete_task(0)
    completed_task = core.list_tasks()[0]
    assert completed_task["done"] is True
    
    removed = core.remove_task(0)
    assert removed["title"] == "Clean room"
    
    remaining_tasks = core.list_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0]["title"] == "Do laundry"

def test_task_persistence(monkeypatch):
    # Use a temporary file for isolation
    test_file = "test_persist_tasks.json"
    monkeypatch.setattr(storage, "TASKS_FILE", test_file)

    # Clean up any existing file
    if os.path.exists(test_file):
        os.remove(test_file)

    # Add a task and simulate saving to disk
    task = core.add_task("Persistent task")

    # Simulate a "restart" by reloading tasks
    reloaded_tasks = core.list_tasks()

    assert len(reloaded_tasks) == 1
    assert reloaded_tasks[0]["title"] == "Persistent task"
    assert reloaded_tasks[0]["done"] is False

    # Cleanup test file
    os.remove(test_file)

