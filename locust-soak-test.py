import logging
import random
import json
from locust import HttpUser, task, constant, LoadTestShape, SequentialTaskSet

queries_list = []
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class UserQuery(SequentialTaskSet):

    @task
    def demo_post_test(self):
        post_url = "/api/users"

        request_body = {
            "query": random.choice(queries_list),
            "job": "leader"
        }
        response = self.client.post(post_url, request_body, name='Entitle Query')
        jsonobj = json.loads(response.json())
        logging.info("Response Count is %s", len(jsonobj["c"]))


class DemoHttpUser(HttpUser):
    tasks = [UserQuery]
    constant(2)
    host = "https://reqres.in"


class StagesShape(LoadTestShape):
    """
    A simple load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        {"duration": 60, "users": 100, "spawn_rate": 10},
        {"duration": 400, "users": 500, "spawn_rate": 10},
        {"duration": 440, "users": 0, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
