# Celery Distributed Task Queue with FastAPI for Machine Learning
Ref: https://github.com/katanaml/sample-apps/tree/master/11

This sample app demonstrates how to implement Celery distributed task queues on top of RabbitMQ broker for Machine Learning model training and data processing. We are using TensorFlow in this example to train the model. API request comes through FastAPI and it is being processed asynchronously by Celery. There is a separate API endpoint to check task status. Multiple requests can be initiated and processed at the same time in parallel. Celery tasks can be monitored using Flower monitoring tool.

* Celery [documentation](https://docs.celeryproject.org/en/stable/index.html)
* [Flower](https://flower.readthedocs.io/en/latest/) - Celery monitoring tool

## Important Notes
1. Folder structure
```
celery-demo/
├─ task/                  # submodule `task` to be demo
│  ├─ __init__.py         # make task a mmodule
│  ├─ tasks.py            # implement tasks
│  ├─ worker.py           # celery.worker
├─ endpoint.py            # fastapi entry point
├─ models.py              # pydantic data validation 
├─ router.py              # specify path to submodule `task`
├─ directly_add_task.py
├─ README.md
```
2. Celery worker and worker processes are different things (Read this for reference). When a worker is started it then spawns a certain number of child processes. The default number of those processes is equal to a number of cores on that machine.
```
$ celery -A proj worker -l info --concurrency=4 -n wkr1@hostname
$ celery -A proj worker -l info --concurrency=2 -n wkr2@hostname
$ celery -A proj worker -l info --concurrency=2 -n wkr3@hostname
```
1. You can check tasks in rabbitmq by `rabbitmqctl list_queues`

## Create vhost in RabbitMQ
1. Check `rabbitmqctl list_vhosts`
2. Create vhost: `rabbitmqctl add_vhost <vhostName>`
   1. e.g. `rabbitmqctl add_vhost task`
3. Restart vhost by `rabbitmqctl restart_vhost --vhost <vhostName>`

## Registor Users in RabbitMQ
1. For windows, cd to `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.11.9\sbin`
2. `rabbitmqctl list_users`
   1. If you failed on Windows:
      Ref: https://stackoverflow.com/questions/47874958/rabbitmq-failed-to-start-tcp-connection-succeeded-but-erlang-distribution-faile
      1. copy the .erlang.cookie file from C:\Windows\System32\config\systemprofile paste it into C:\Users\["your user nameusername"] folder
      2. run `rabbitmq-service.bat stop` and `rabbitmq-service.bat start`
3. Create users: `rabbitmqctl add_user <userName> <password>`
4. Set administrator: `rabbitmqctl set_user_tags <userName> administrator`
5. Set permission to vhost: `rabbitmqctl set_permissions [-p <vhost>] <user> <conf> <write> <read>`
   1. e.g. `rabbitmqctl set_permissions -p task worker ".*" ".*" ".*"`

## Commands
* Two ways to add tasks:
  * Start FastAPI endpoint
    * `python3 -m uvicorn endpoint:app --reload`
  * Directly call with celery
    * `python3 directly_add_task.py`
* Start Celery worker
  * **python3 -m celery -A task.worker.app worker --pool=solo --loglevel=INFO -n <worker_name>**
    * e.g. `python3 -m celery -A task.worker.app worker --pool=solo --loglevel=INFO -n worker1@main`
* Start Flower monitoring dashboard
  * **python3 -m celery -A task.worker --broker=amqp://worker:worker@localhost:5672/task flower --port=5555**



## URL's

* API url: http://127.0.0.1:8000/api/v1/task/docs
* Flower url: http://127.0.0.1:5555
