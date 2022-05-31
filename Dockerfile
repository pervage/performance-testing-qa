FROM python:latest

ARG TEST_TYPE
ENV TEST_TYPE = ${TEST_TYPE}
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT /usr/src/app/entrypoint.sh