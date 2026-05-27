import json
import os
import sys

DB_FILE = "todos.json"

def load_todos():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_todos(todos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)

def list_todos():
    todos = load_todos()
    if not todos:
        print("No todos yet.")
        return
    for i, t in enumerate(todos, start=1):
        mark = "✓" if t["done"] else " "
        print(f"{i}. [{mark}] {t['text']}")

def add_todo(text):
    todos = load_todos()
    todos.append({"text": text, "done": False})
    save_todos(todos)
    print(f'Added: "{text}"')

def mark_done(n):
    todos = load_todos()
    if n < 1 or n > len(todos):
        print("Invalid todo number.")
        return
    todos[n - 1]["done"] = True
    save_todos(todos)
    print(f"Marked #{n} as done.")

def remove_todo(n):
    todos = load_todos()
    if n < 1 or n > len(todos):
        print("Invalid todo number.")
        return
    removed = todos.pop(n - 1)
    save_todos(todos)
    print(f'Removed: "{removed["text"]}"')

def clear_completed():
    todos = load_todos()
    before = len(todos)
    todos = [t for t in todos if not t["done"]]
    removed_count = before - len(todos)
    save_todos(todos)
    print(f"Cleared {removed_count} completed todo(s).")

def show_stats():
    todos = load_todos()
    total = len(todos)
    completed = sum(1 for t in todos if t["done"])
    pending = total - completed
    print(f"Total: {total}")
    print(f"Completed: {completed}")
    print(f"Pending: {pending}")

def main():
    if len(sys.argv) < 2:
        print('Usage: python todo.py [list|add|done|remove|clear|stats] [args]')
        return

    cmd = sys.argv[1]
    if cmd == "list":
        list_todos()
    elif cmd == "add":
        if len(sys.argv) < 3:
            print('Usage: python todo.py add "task"')
            return
        add_todo(" ".join(sys.argv[2:]))
    elif cmd == "done":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Usage: python todo.py done <number>")
            return
        mark_done(int(sys.argv[2]))
    elif cmd == "remove":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Usage: python todo.py remove <number>")
            return
        remove_todo(int(sys.argv[2]))
    elif cmd == "clear":
        clear_completed()
    elif cmd == "stats":
        show_stats()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
