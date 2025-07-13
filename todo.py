import json
import datetime
from colorama import Fore, Style, init
from plyer import notification

init(autoreset=True)

TASKS_FILE = "data.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

# Display all tasks
def display_tasks(tasks):
    if not tasks:
        print(Fore.YELLOW + "No tasks yet.")
        return
    for i, task in enumerate(tasks):
        status = Fore.GREEN + "✔ Done" if task["completed"] else Fore.RED + "✘ Pending"
        print(f"{i+1}. {Fore.CYAN}{task['title']} ({task['due_date']}) - Assigned to {task['assigned_to']} - Priority: {task['priority']} - {status}")

# Add a new task
def add_task(tasks):
    title = input("Task Title: ")
    due = input("Due Date (YYYY-MM-DD): ")
    assigned_to = input("Assign To: ")
    priority = input("Priority (Low/Medium/High): ").capitalize()

    task = {
        "title": title,
        "due_date": due,
        "assigned_to": assigned_to,
        "priority": priority,
        "completed": False
    }
    tasks.append(task)
    print(Fore.GREEN + "Task added!")

# Mark task as complete
def complete_task(tasks):
    display_tasks(tasks)
    index = int(input("Enter task number to mark as done: ")) - 1
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        print(Fore.GREEN + "Task marked as completed!")

# Show upcoming tasks
def show_due_soon(tasks):
    today = datetime.date.today()
    for task in tasks:
        due = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        if due <= today and not task["completed"]:
            notification.notify(
                title=" Task Due Today!",
                message=f"{task['title']} (Assigned to {task['assigned_to']})",
                timeout=5
            )
            print(Fore.YELLOW + f"[Reminder] {task['title']} is due today!")

# Menu
def main():
    tasks = load_tasks()

    while True:
        print(Style.BRIGHT + "\n=== Team To-Do List ===")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Check Due Tasks Today")
        print("5. Save & Exit")

        choice = input("Choose option: ")

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            show_due_soon(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print(Fore.CYAN + "Tasks saved. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")

if __name__ == "__main__":
    main()
