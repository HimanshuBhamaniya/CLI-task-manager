import json
from datetime import datetime
import argparse

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: {description}  ID:({len(tasks)})")

def update_task(id, new_description):
    tasks = load_tasks()
    id = int(id)
    tasks[id - 1].update({"description": new_description})
    tasks[id - 1].update({"updated_at": datetime.now().isoformat()})
    save_tasks(tasks)
    print(f"Task {id} updated: {new_description}")

def delete_task(id):
    tasks = load_tasks()
    id = int(id)
    tasks.pop(id - 1)
    save_tasks(tasks)
    print("Task deleted successfully")

def mark_task(id, new_status):
    tasks = load_tasks()
    id = int(id)
    if new_status not in {"todo", "in-progress", "done"}:
        raise TypeError('Invalid operation')
    tasks[id - 1].update({"status": new_status})
    tasks[id - 1].update({"updated_at": datetime.now().isoformat()})
    save_tasks(tasks)
    print(f"{tasks[id - 1]['description']} : {new_status}")

def list_tasks():
    tasks = load_tasks()
    for t in tasks:
        print(f"{t['id']} {t['description']} {t['status']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # update
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", help="Task ID")
    update_parser.add_argument("description", help="New description")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")

    # mark
    mark_parser = subparsers.add_parser("mark", help="Change task status")
    mark_parser.add_argument("id", help="Task ID")
    mark_parser.add_argument("status", help="New status (todo, in-progress, done)")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark":
        mark_task(args.id, args.status)