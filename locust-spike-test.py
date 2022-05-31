import logging
import math
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
