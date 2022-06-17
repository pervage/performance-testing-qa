import json
import logging
import math
import os

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


class DoubleWave(LoadTestShape):
    """
    A shape to imitate some specific user behaviour. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3
    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 20
    peak_one_users = 60
    peak_two_users = 40
    time_limit = 600

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                    (self.peak_one_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                    + (self.peak_two_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                    + self.min_users
            )
            return round(user_count), round(user_count)
        else:
            return None
