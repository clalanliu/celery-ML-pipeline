from models import RequestData, Task, Result
from celery.result import AsyncResult
from task.tasks import train_model
import asyncio
import time
def run_training(requestData:RequestData):
    task_id = train_model.delay(requestData.test_size)
    return {'task_id': str(task_id), 'status': 'Processing'}

task_id_in_queue = []
for i in range(10):
    requestData = RequestData(test_size=i*0.05+0.01)
    response = run_training(requestData)
    task_id_in_queue.append(response['task_id'])

while len(task_id_in_queue) > 0:
    for task_id_idx in range(len(task_id_in_queue) - 1, -1, -1):
        task = AsyncResult(task_id_in_queue[task_id_idx])
        if task.ready():
            result = task.get()
            del task_id_in_queue[task_id_idx]
    
    print(f"{len(task_id_in_queue)} in queue ...")
    time.sleep(1)