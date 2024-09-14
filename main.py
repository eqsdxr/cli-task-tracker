import argparse
import json
import datetime


# Get and parse terminal commands
parser = argparse.ArgumentParser()

parser.add_argument('command')
parser.add_argument('task_id_or_mode_or_description', nargs='?', default=None)
parser.add_argument('description', nargs='?', default=None)

args = parser.parse_args()


# Current date function
def current_time()->str:
    return datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")


# Check if the JSON file exists
def check_if_json_exists()->bool:
    try:
        with open('data.json', 'r') as file:
            json.load(file)
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        with open("data.json", "w") as file:
            json.dump({}, file)
        return False


# Rearrange task IDs
def rearrange_task_ids(tasks: dict)->None:
    rearranged_tasks = {index: tasks[key] for index, key in enumerate(tasks)}
    with open('data.json', 'w') as file:
        json.dump(rearranged_tasks, file, indent=4)


# Add a task
def add_task(description: str, status: str, tasks: dict) -> str:
    created_time = current_time()
    task_id = len(tasks)
    tasks[task_id] = {
        "description": description,
        "status": status if status else 'todo',
        "last modified": created_time
        }
    with open("data.json", "w") as file:
        json.dump(tasks, file, indent=4)
    return f"Successfully added:\nid: {task_id}\ndescription: \"{description}\"\nstatus: {status if status else 'todo'}\ncreated: {created_time}"


# Check if a task exists
def check_if_task_exists(task_id: str, tasks: dict) -> bool:
    return task_id in tasks


# Update a task
def update_task(task_id: str, description: str, tasks: dict) -> str:
    if check_if_task_exists(task_id, tasks):
        old_description = tasks[task_id]["description"]
        tasks[task_id]["description"] = description
        tasks[task_id]["last modified"] = current_time()
        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)
        if old_description == description:
            return f"Task with id {task_id} already has this description.\n{old_description} => X"
        return f"Task {task_id} updated.\n{old_description} => {description}"
    else:
        return f"Task {task_id} not found."


# Delete a task
def delete_task(task_id: str, tasks: dict) -> str:
    if '.' in task_id:
        task_ids = task_id.split('.')
        result = []
        for task_id in task_ids:
            if check_if_task_exists(task_id, tasks):
                deleted_task = {
                    'description': tasks[task_id]['description'],
                    'status': tasks[task_id]['status'],
                    'last modified': tasks[task_id]['last modified']
                }
                del tasks[task_id]
                result.append(f"{task_id} ; {deleted_task['description']} ; {deleted_task['status']} ; {deleted_task['last modified']}")
            else:
                result.append(f"Task with id \"{task_id}\" not found.")
        rearrange_task_ids(tasks)
        result.insert(0, 'Deleted tasks:')
        result.append('*task IDs were rearranged')
        return [result, "list"]
    else:
        if check_if_task_exists(task_id, tasks):
            deleted_task = {
                'description': tasks[task_id]['description'],
                'status': tasks[task_id]['status'],
                'last modified': tasks[task_id]['last modified']
            }
            del tasks[task_id]
            rearrange_task_ids(tasks)
            return f"A task was deleted.\nid: {task_id}\ndescription: {deleted_task['description']}\nstatus: {deleted_task['status']}\nlast modified: {deleted_task['last modified']}\n*task IDs were rearranged"
        else:
            return f"Task with id \"{task_id}\" not found."


# List tasks
def list_tasks(status: str, tasks: dict) -> dict:
    if not tasks:
        return "No tasks available."
    if status:
        filtered_tasks = {key: task for key, task in tasks.items() if task['status'] == status}
        if filtered_tasks:
            return filtered_tasks
        return f'There\'s no tasks with the status "{status}"'
    return tasks


# Mark task as done/in-progress/todo/neglected/etc.
def mark_task(task_id: str, status: str, tasks: dict) -> list:
    if check_if_task_exists(task_id, tasks):
        old_status = tasks[task_id]["status"]
        old_last_modified = tasks[task_id]["last modified"]
        tasks[task_id]["status"] = status
        tasks[task_id]["last modified"] = current_time()
        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)
        return f'id: {task_id}\nstatus: "{old_status}" => "{status}"\n"{tasks[task_id]["description"]}"\nlast modified: {old_last_modified} => {tasks[task_id]["last modified"]}'
    return f"Task {task_id} not found."


# Main function
def main(command, task_id_or_mode_or_description=None, description=None, status=None):
    if check_if_json_exists():
        with open('data.json', 'r') as file:
            tasks = json.load(file)

        if command.lower() == "add":
            print(add_task(task_id_or_mode_or_description, str(description), tasks))

        elif command.lower() == "update":
            if task_id_or_mode_or_description is None or description is None:
                print("Task ID and description are required for updating.")
                return
            print(update_task(task_id_or_mode_or_description, str(description), tasks))

        elif command.lower() == "delete":
            result = delete_task(task_id_or_mode_or_description, tasks)
            if result[1] == "list":
                for i in result[0]:
                    print(i)
            else:
                print(result)
        elif command.lower() == "list":
            tasks_to_list = list_tasks(task_id_or_mode_or_description, tasks)
            if isinstance(tasks_to_list, str):
                print(tasks_to_list)
            else:
                for key, task in tasks_to_list.items():
                    print(f"{key}; {task['status']}; {task['last modified']}; {task['description']}")

        elif command.lower() == 'mark':
            print(mark_task(task_id_or_mode_or_description, description, tasks))
        else:
            print('the command was unrecognized')
    else:
        print("JSON file didn't exist. Now it exist and you can add new tasks.")


main(args.command, args.task_id_or_mode_or_description, args.description)
