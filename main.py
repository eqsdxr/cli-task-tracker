import argparse, json, datetime, os

parser = argparse.ArgumentParser()

parser.add_argument('a1')
parser.add_argument('a2', default="Nothing")
# parser.add_argument('a3', default="Nothing")

args = parser.parse_args()

content = {}

# print(args.a1)
# print(args.a2)
# print(args.a3)


# CHEATSHEATS

# task_cli add|delete "buy groceries"
# task_cli update 1 "study instead"
# task_cli mark-done|mark-todo|mark-in-progress|mark-not-in-progress 1
# task_cli list
# task_cli list done|todo|in-progress

# & C:/Users/Студент/AppData/Local/Programs/Python/Python312/python.exe "c:/Users/Студент/Desktop/Ivan Smagin/task tracker/main.py" update 1 "Hi!"

#JSON
# {
#     "1": {"description": ????, "status": ????, "modification_data": ????}
# }


# FUNCTIONS THAT CHECK FILES' EXISTENCE

def check_if_json_exist()->bool:
    try:
        with open("data.json", "r") as file:
            if os.path.getsize(data.json) > 0:
                return "OK"
            else:
                raise Exception
    except:
        with open("data.json", "w") as file:
            pass
        return False


# FUNCTIONS FOR ADDING TASK

def json_add(description):
    with open("data.json", "r") as file:
        content = json.load(file)
    with open("data.json", "w") as file:
        content[len(content)] = {"description": description, "status": "todo", "date": str(datetime.date.today().strftime("%Y-%m-%d"))}
        json.dump(content, file, indent=4)
    print("successfully added")

def json_add_when_no_tasks(description):
    with open("data.json", "w") as file:
        to_add = {"0": {"description": description, "status": "todo", "date": str(datetime.date.today().strftime("%Y-%m-%d"))}}
        json.dump(to_add, file, indent=4)   
    print("successfully added")
    

# MAIN FUNCTION

def main(a1, a2=None, a3=None):
    # print(a1, a2, a3)
    # JSON
    if a1 == "add":
        if check_if_json_exist() == "OK":
            json_add(a2)
        else:
            json_add_when_no_tasks(a2)
    elif a1 == "update":
        if check_if_json_exist() == "OK":
    

main(args.a1, args.a2) # , args.a3