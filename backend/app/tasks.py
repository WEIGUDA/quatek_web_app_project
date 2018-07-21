import time


def example(seconds):
    print('start a task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('task finished')
