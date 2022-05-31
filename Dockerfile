FROM python:latest

ARG TEST_TYPE
ENV TEST_TYPE = ${TEST_TYPE}
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT["locust","-f /usr/src/app/locust-${TEST_TYPE}-test.py --headless --only-summary --html /usr/src/app/output/output-${TEST_TYPE}.html"]