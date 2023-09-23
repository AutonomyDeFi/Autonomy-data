
class TaskManager:
    def __init__(self):
        self.task_list = deque([])
        self.task_id_counter = 1

    def add_task(self, task: dict):
        self.task_list.append(task)

    def process_next_task(self):
        return self.task_list.popleft()

    def create_new_tasks(self, new_tasks: list):
        for new_task in new_tasks:
            self.task_id_counter += 1
            new_task.update({"task_id": self.task_id_counter})
            self.add_task(new_task)

    def print_task_list(self):
        print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
        for task in self.task_list:
            print(f"{task['task_id']}: {task['task_name']}")

