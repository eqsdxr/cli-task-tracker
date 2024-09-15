import argparse
import json
import datetime


# Get and parse terminal commands
parser = argparse.ArgumentParser(description='cli task tracker. ID are assigned automaticaly.')

parser.add_argument('command', help='add/update/delete/mark/list')
parser.add_argument('a2', nargs='?', default=None, help='with add: description; with update/mark: task_id; with delete: ID or ID.ID2.ID3;  with list: status;')
parser.add_argument('a3', nargs='?', default=None, help='with add: status; with update: new_description; with mark: new_status;')

args = parser.parse_args()

# Rearrange task IDs

def rearrange_task_ids(tasks: dict)->str:
    rearranged_tasks = {index: tasks[key] for index, key in enumerate(tasks)}
    with open('data.json', 'w') as file:
        json.dump(rearranged_tasks, file, indent=4)
    return 'task IDs successfully rearranged'

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


# Add a task
def add_task(description: str, status: str, tasks: dict) -> str:
    created_time = current_time()
    try:
        task_id = int(next(reversed(tasks)))+1
    except:
        if not tasks:
            task_id = 0
    status = (None if status.lower() == "none" else status) if status else 'todo' # if a person want to add None as a status they can do it
    tasks[task_id] = {
        "description": description,
        "status": status,
        "created": created_time,
        "last modified": created_time
        }
    with open("data.json", "w") as file:
        json.dump(tasks, file, indent=4)
    return f"Successfully added:\nid: {task_id}\ndescription: \"{description}\"\nstatus: {status}\ncreated: {created_time}"


# Check if a task exists
def check_if_task_exists(task_id: str, tasks: dict) -> bool:
    return task_id in tasks


# Update a task
def update_task(task_id: str, description: str, tasks: dict) -> str:
    if '-' in task_id:
        return "task id can't be less than 0"
    if task_id == '-0':
        task_id = '0'
    if check_if_task_exists(task_id, tasks):
        old_description = tasks[task_id]["description"]
        old_last_modified = tasks[task_id]["created"]
        tasks[task_id]["description"] = description
        tasks[task_id]["last modified"] = current_time()
        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)
        if old_description == description:
            return f"Task with id {task_id} already has this description.\ndescription: {old_description} => {old_description}"
        return f"Successfully updated:\nid: {task_id}\ndescription: \"{old_description}\" => \"{description}\"\nstatus: {tasks[task_id]['status']}\ncreated: {tasks[task_id]['created']}\nlast modified: {old_last_modified} => {tasks[task_id]['last modified']}"
    else:
        return f"Task {task_id} not found."


# Delete a task
def delete_task(task_id: str, tasks: dict) -> str:
    if not task_id:
        return 'task id is required'
    if '-' in task_id:
        return "task id can't be less than 0"
    if task_id == '-0':
        task_id = '0'
    if '.' in task_id:
        task_ids = task_id.split('.')
        result = []
        for task_id in task_ids:
            if check_if_task_exists(task_id, tasks):
                deleted_task = {
                    'description': tasks[task_id]['description'],
                    'status': tasks[task_id]['status'],
                    'last modified': tasks[task_id]['last modified'],
                    'created': tasks[task_id]['created']
                }
                del tasks[task_id]
                result.append(f"{task_id} ; {deleted_task['description']} ; {deleted_task['status']} ; last modified: {deleted_task['last modified']} ; created: {deleted_task['created']}")
            else:
                result.append(f"Task with id \"{task_id}\" not found.")
        with open('data.json', 'w') as file:
            json.dump(tasks, file, indent=4)
        result.insert(0, 'Deleted tasks:')
        return [result, "multiple_deleting"]
    else:
        if check_if_task_exists(task_id, tasks):
            deleted_task = {
                'description': tasks[task_id]['description'],
                'status': tasks[task_id]['status'],
                'last modified': tasks[task_id]['last modified'],
                'created': tasks[task_id]['created']
            }
            del tasks[task_id]
            with open('data.json', 'w') as file:
                json.dump(tasks, file, indent=4)
            return f"A task was deleted.\nid: {task_id}\ndescription: {deleted_task['description']}\nstatus: {deleted_task['status']}\nlast modified: {deleted_task['last modified']}\ncreated: {deleted_task['created']}"
        else:
            return f"Task with id \"{task_id}\" not found."


# List tasks
def list_tasks(status: str, tasks: dict) -> dict:
    if not tasks:
        return "No tasks available."
    if status:
        if status.lower() == "None":
            status = None
    if status:
        filtered_tasks = {key: task for key, task in tasks.items() if task['status'] == status}
        if filtered_tasks:
            return filtered_tasks
        return f'There\'s no tasks with the status "{status}"'
    return tasks


# Mark task as done/in-progress/todo/neglected/etc.
def mark_task(task_id: str, status: str, tasks: dict) -> list:
    if not task_id:
        return 'task_id is required'
    if '-' in task_id:
        return "task id can't be less than 0"
    if check_if_task_exists(task_id, tasks):
        if status == None: # this code prevent error in the next elif because None doesn't have .lower()
            pass
        elif status.lower() == "none": # if a user wants to change status of a task to None then they can do it
            status = None
        old_status = tasks[task_id]["status"]
        tasks[task_id]["status"] = status
        if old_status == status:
            return f"this task already has this status\nid: {task_id}\nstatus: {old_status} => {old_status}"
        old_last_modified = tasks[task_id]["last modified"]
        tasks[task_id]["last modified"] = current_time()
        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)
        return f'id: {task_id}\nstatus: "{old_status}" => "{status}"\n"{tasks[task_id]["description"]}"\nlast modified: {old_last_modified} => {tasks[task_id]["last modified"]}\ncreated: {tasks[task_id]["created"]}'
    return f"Task {task_id} not found."


# Main function
def main(command, a2=None, a3=None):
    if check_if_json_exists():
        with open('data.json', 'r') as file:
            tasks = json.load(file)

        if command.lower() == "add":
            print(add_task(str(a2), a3, tasks))

        elif command.lower() == "update":
            if a2 is None or a3 is None:
                print("Task ID and new description are required for updating.")
                return
            print(update_task(a2, str(a3), tasks))

        elif command.lower() == "delete":
            result = delete_task(a2, tasks)
            if result[1] == "multiple_deleting": # printing of returned tasks if multiple tasks were deleted
                for i in result[0]:
                    print(i)
            else:
                print(result)
        elif command.lower() == "list":
            tasks_to_list = list_tasks(a2, tasks)
            if isinstance(tasks_to_list, str):
                print(tasks_to_list)
            else:
                for key, task in tasks_to_list.items():
                    print(f"{key}; {task['status']}; {task['created']} ; {task['last modified']} ; {task['description']}")

        elif command.lower() == 'mark':
            print(mark_task(a2, a3, tasks))
        elif command.lower() == 'rearrange':
            if a2: # a3 can't exist if a2 doesn't exist.
                useless_argumnets = (f'"{a2}", "{a3}"') if a3 else (f'"{a2}"')
                print(f'*The function accepted given arguments ({useless_argumnets}), but they are not usable in the function\'s logic.')
            print(rearrange_task_ids(tasks))
            with open('data.json', 'r') as file: # open again in order to read the new indexes of taskss.
                tasks = json.load(file)
            tasks_to_list = list_tasks(None, tasks)
            if isinstance(tasks_to_list, str): # print tasks
                print(tasks_to_list)
            else:
                for key, task in tasks_to_list.items():
                    print(f"{key}; {task['status']}; {task['created']} ; {task['last modified']} ; {task['description']}")
        else:
            print('the command was unrecognized')
    else:
        print("JSON file didn't exist. Now it exist and you can add new tasks.")


main(args.command, args.a2, args.a3)
