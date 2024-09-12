import argparse, json, datetime, os


# geting and parsing terminal commands
parser = argparse.ArgumentParser()

parser.add_argument('a1')
parser.add_argument('a2', nargs='?')
parser.add_argument('a3', nargs='?')

args = parser.parse_args()

# content = {}

# print(args.a1)
# print(args.a2)
# print(args.a3)


# CHEATSHEATS

# task_cli add|delete "buy groceries"
# task_cli update 1 "study instead"
# task_cli mark-done|mark-todo|mark-in-progress|mark-not-in-progress
# task_cli list
# task_cli list done|todo|in-progress

# & C:/Users/Студент/AppData/Local/Programs/Python/Python312/python.exe "c:/Users/Студент/Desktop/Ivan Smagin/task tracker/main.py" update 1 "Hi!"

#JSON
# {
#     "1": {"description": ????, "status": ????, "modification_data": ????}
# }


# DATE FUNCTION

def current_time()->str:
    return (datetime.datetime.now().strftime("%Y-%m-%d--%H-%M"))


# FUNCTIONS THAT CHECK FILES' EXISTENCE

def check_if_json_exist()->bool:
    try:
        if os.path.getsize("data.json") > 0:
            return "OK"
        else:
            raise Exception
    except:
        with open("data.json", "w") as file:
            pass
        return False

# FUNCTIONS THAT REARRANGE TASKS' IDs

def rearrange_task_ids():
    with open('data.json', 'r') as file:
        tasks_from_json = json.load(file)
    task_keys = tasks_from_json.keys()
    index = 0
    for key in task_keys:
        tasks_from_json[index] = tasks_from_json[key]
        index += 1
    with open('data.json', 'w') as file:
        json.dump(tasks_from_json)

# FUNCTIONS FOR ADDING TASK

def task_add(description, status=None):
    # this function doesn't need to check if a task exist
    with open("data.json", "r") as file:
        tasks_from_json = json.load(file)
    with open("data.json", "w") as file:
        if status == None:
            status = 'todo'
        tasks_from_json[len(tasks_from_json)] = {"description": description, "status": status, "last modified": current_time()}
        json.dump(tasks_from_json, file, indent=4)
    print("successfully added")

def task_add_when_no_tasks(description, status="todo"):
    with open("data.json", "w") as file:
        last_modified = current_time() # this function should exist because there are two outputs of date and they should be identical
        to_add = {"0": {"description": description, "status": status, "last modified": last_modified}}
        json.dump(to_add, file, indent=4)   
    print(f"json file didn't exist so one was created and there is only one your task: \nid: 0\ndescription: {description}\nstatus: {status}\nlast modified: {last_modified}")
        


# CHECK IF A TASK EXIST

def check_if_a_task_exist(task_id):
    with open("data.json", "r") as file:
        tasks_from_json = json.load(file)
        if tasks_from_json[task_id]:
            return "OK"
        else:
            return False


# UPDATE FUNCTIONS

def json_update(a2, a3):
    if check_if_a_task_exist(a2) == "OK":
        with open("data.json", "r") as file:
            tasks_from_json = json.load(file)
            tasks_from_json[a2]["description"] = a3
            tasks_from_json[a2]["last modified"] = current_time()
        with open("data.json", "w") as file:
            json.dump(tasks_from_json, file, indent=4)
        return "success"
    else:
        return "task id doesn't exist"


# DELETE FUNCTION # WORKS PROPERLY

def json_task_delete(task_id):
    if check_if_a_task_exist(task_id) == "OK":
        with open("data.json", "r") as file:
            tasks_from_json = json.load(file)
            status = tasks_from_json[task_id]['status']
            description = tasks_from_json[task_id]['description']
            last_modified = tasks_from_json[task_id]['last modified']
        with open("data.json", "w") as file:
            json.dump(tasks_from_json, file, indent=4)
            return f"a task was deleted \nid: \"{task_id}\"\ndescription: \"{description}\"\nstatus:{status}\nlast modification time:{last_modified}"
        rearrange_task_ids()
    else:
        return f"the task with id \"{task_id}\" doesn't exist"


# LIST FUNCTIONS

def task_list(mode=None):
    if mode == None or (mode).lower() == 'none':
        with open('data.json', 'r') as file:
            task_list = json.load(file)
        return task_list
    else:
        with open('data.json', 'r') as file:
            former_task_list = json.load(file)
            new_task_list = {}
            for i in former_task_list:
                if former_task_list[i]['status'] == mode:
                    new_task_list[i] = former_task_list[i]
        if len(new_task_list) >= 1:
            return new_task_list
        else:
            return "There's no any task with this status"

    
# MARK FUNCTION # ADD ID PRINT FUNCTION AND CORECT THE PRINTING

def mark_function(task_id, new_status):
    if check_if_a_task_exist(task_id) == "OK":
        with open('data.json', 'r') as file:
            task_list = json.load(file)
        task_list[task_id]['status'] = new_status
        task_list[task_id]['last modified'] = current_time()
        with open('data.json', 'w') as file:
            json.dump(task_list, file, indent=4)            
        return task_list[task_id]
    else:
        return "task with this id doesn't exist"
    
    
# MAIN FUNCTION

def main(a1, a2=None, a3=None):
    if check_if_json_exist() == "OK":
        if a1.lower() == "add":  # make output beautiful
            task_add(a2, a3)
        elif a1.lower() == "update":  # make output beautiful
            print(json_update(a2, a3))
        elif a1.lower() == "delete":  # make output beautiful
            print(json_task_delete(a2))
        elif a1.lower() == "list":  # make output beautiful
            print(task_list(a2))
        elif a1.lower() == 'mark':  # make output beautiful
            print(mark_function(a2, a3))
    elif a1.lower() == "add":  # make output beautiful
        task_add_when_no_tasks(a2, a3)
    else:
        print("json file doesn't exist, so no tasks can be deleted/updated/marked/printed. \n now json file does exist and you can add new tasks there")


main(args.a1, args.a2, args.a3)