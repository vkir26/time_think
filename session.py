from core import main, get_task


def run() -> str:
    attempts = 5
    wrong_answer = 0
    correct_answer = 0

    task = get_task()
    for i in range(attempts):
        if wrong_answer != 3:
            print(task)
            user_answer = int(input())
            if main(task, user_answer):
                print("Correct")
                correct_answer += 1
                task = get_task()
            else:
                print("Not correct")
                wrong_answer += 1

    return f"Correct: {correct_answer}\nWrong: {wrong_answer}"
