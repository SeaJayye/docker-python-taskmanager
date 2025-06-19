# main.py

from task_manager import core

def main():
    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Remove Task")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task title: ")
            core.add_task(title)
        elif choice == "2":
            tasks = core.list_tasks()
            for i, task in enumerate(tasks):
                status = "✓" if task["done"] else "✗"
                print(f"{i}. [{status}] {task['title']}")
        elif choice == "3":
            index = int(input("Task index to mark complete: "))
            try:
                core.complete_task(index)
            except IndexError:
                print("Invalid index.")
        elif choice == "4":
            index = int(input("Task index to remove: "))
            try:
                core.remove_task(index)
            except IndexError:
                print("Invalid index.")
        elif choice == "5":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
    