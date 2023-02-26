from celery import Celery
import argparse
import sys
from click import Option
from celery import bootsteps

class MyBootstep(bootsteps.Step):
    def __init__(self, parent, cuda_id=0, **options):
        super().__init__(parent, **options)
        print(f"cuda_id is {cuda_id}")

app = Celery(
    'celery_web',
    broker=f'pyamqp://worker:worker@localhost/task',
    backend='rpc://', 
    include=['task.tasks'],
)

app.user_options['worker'].add(Option(('--cuda_id',),
                                      default=0))
app.steps['worker'].add(MyBootstep)

if __name__ == '__main__':
    app.start()
