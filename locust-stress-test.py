import logging
import os
import json
from locust import HttpUser, task, constant, LoadTestShape, SequentialTaskSet

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
json_file = open(os.path.abspath("perf-test-data.json"))
json_data = json.load(json_file)


class UserQuery(SequentialTaskSet):

    @task
    def filter_query_test(self):
        for body_data in json_data["loadTestData"]["filterQuery"]:
            post_url = "/generic/filter-query"
            headers = {'content-type': 'application/json'}
            request_body = {
                "query": body_data["query"],
                "domain": body_data["domain"]
            }
            print(request_body)
            response = self.client.post(post_url, json=request_body, name=body_data["testCaseId"], headers=headers)
            jsonobj = response.json()
            logging.info("Response Count is %s", len(jsonobj["c"]))

    @task
    def count_query_test(self):
        for body_data in json_data["loadTestData"]["countQuery"]:
            post_url = "/generic/count"
            headers = {'content-type': 'application/json'}
            request_body = {
                "query": body_data["query"]
            }
            print(request_body)
            response = self.client.post(post_url, json=request_body, name=body_data["testCaseId"], headers=headers)
            jsonobj = response.json()
            logging.info("Response Count is %s", len(jsonobj["c"]))


class LoadTestUser(HttpUser):
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
        {"duration": 60, "users": 10, "spawn_rate": 10},
        {"duration": 100, "users": 50, "spawn_rate": 10},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 220, "users": 30, "spawn_rate": 10},
        {"duration": 230, "users": 10, "spawn_rate": 10},
        {"duration": 240, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
