import random


class Task:
    def __init__(self):
        self.task = generate_task()

    def generate(self):
        return self.task

class Answer:
    pass

def generate_task() -> list[int]:
    return sorted([random.randint(1, 5) for _ in range(2)])

def answer_validator(ready_task: Task, answer: Answer) -> bool:
    pass

if __name__ == "__main__":
    task = Task()
    print(task.generate())