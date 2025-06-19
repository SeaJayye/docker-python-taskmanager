from .storage import load_tasks, save_tasks

def add_task(title):
    tasks = load_tasks()
    new_task = {"title": title, "done": False}
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No current tasks.")
        return []
    return tasks

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        return tasks[index]
    raise IndexError("Task index out of range.")

def remove_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        return removed
    raise IndexError("Task index out of range.")
