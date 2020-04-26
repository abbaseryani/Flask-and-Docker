from celery import Celery

app = Celery("tasks", broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

@app.task
def reverse(wort):
    return wort[::-1]