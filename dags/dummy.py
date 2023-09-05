from airflow.decorators import task, dag
from datetime import datetime

@dag(schedule_interval=None, start_date=datetime(2023, 9, 5), catchup=False, tags=["my-dummy-dag"])
def dummy():

    # assume some externally given arguments
    arg_for_A = "input for task A"
    arg_for_B = "input for task B"

    @task(queue='queueA')
    def dummy_task_A(arg: str) -> None:
        print(f"Running dummy task A with arg: {arg}!")
        print("Heavy work being done...")
        # could have various dependencies, e.g. tensorflow

    # Concrete IMPLEMENTATION should not be here, just an interface, as with Celery signatures
    # the worker will have the actual implementation
    # this should just send the serialized inputs & task_id to the right queue
    # Example pseudo-code:
    # @signature(queue='queueA')
    # def dummy_task_A(arg: str) -> None:
    #     pass

    @task(queue='queueB')
    def dummy_task_B(arg: str) -> str:
        print(f"Running dummy task B with arg: {arg}!")
        return "result of complex operation"

    # same for task B, only a request here, not the full implementation
    # @signature(queue='queueB')
    # def dummy_task_B(arg: str) -> str:
    #     pass

    # Call the task functions with arguments fetched from dag_run.conf
    dummy_task_A(arg_for_A)
    result = dummy_task_B(arg_for_B)
    # do whatever with the result...

dummy()
