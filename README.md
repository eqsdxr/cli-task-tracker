# cli-task-tracker

A simple terminal task tracker in python. A project from https://roadmap.sh/projects/task-tracker.

## Features

- **add**: add a new task
- **update**: update description of the task with specific id
- **delete**: remove task with specific id
- **list**: show all tasks with specific status
- **mark**: change the status of task with specific id 

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/eqsdxr/cli-task-tracker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd task-tracker
    ```
3. Ensure you have Python installed. This project is compatible with Python 3.x.

## Usage

Run the script from the command line with the appropriate command and arguments:

- **add**:
    ```bash
    python task_tracker.py add "Task Description" "optional_status"
    ```
- **update**:
    ```bash
    python task_tracker.py update task_id "New Description"
    ```
- **delete**:
    ```bash
    python task_tracker.py delete task_id | id1.id2.id3
    ```
    - You can delete multiple tasks by specifying a list of `task_ids`, separated by dots (e.g., `0.1.2.3.4`).
- **list**:
    ```bash
    python task_tracker.py list [status]
    ```
    - If `status` is omitted, all tasks will be listed.
- **mark**:
    ```bash
    python task_tracker.py mark task_id new_status
    ```

## Example

1. To add a new task:
    ```bash
    python task_tracker.py add "Finish the report" "in-progress"
    ```

2. To list all tasks:
    ```bash
    python task_tracker.py list
    ```

3. To update a task:
    ```bash
    python task_tracker.py update 0 "Complete the report"
    ```

4. To delete a task:
    ```bash
    python task_tracker.py delete 0
    ```

5. To mark a task as completed:
    ```bash
    python task_tracker.py mark 0 completed
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to use, modify, or distribute this project as you wish. Contributions are not required.


## Contact

For any questions or feedback, please open an issue in the GitHub repository or contact [rxdsqe@gmail.com](mailto:rxdsqe@gmail.com).
