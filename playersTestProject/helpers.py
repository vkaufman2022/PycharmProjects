import datetime
import requests
from requests.auth import HTTPBasicAuth


def validate_sequential_ids(page, response, start, end):
    actual_ids = []
    for actual_id in response:
        actual_ids.append(actual_id["ID"])
    for expected_id, actual_id in zip(range(start, end), actual_ids):
        if expected_id - actual_id != 0:
            print("Page {0}: actual player id is {1} ,but expected {2}".format(page, actual_id, expected_id))
            return False
    return True


def validate_names(page, response):
    for actual_player in response:
        if actual_player["Name"] is '':
            print("Page {0}: player id {1} name is empty".format(page, actual_player["ID"]))
            return False
    return True


def send_request(path, user, password, i):
    response = requests.get(path + "{0}".format(i), auth=HTTPBasicAuth(user, password))
    print("Get {0}".format(path + "{0}".format(i)))
    if 200 <= response.status_code < 300:
        print(response.json())
    else:
        print(response)
    return response


def send_request_without_prints(path, user, password, i):
    response = requests.get(path + "{0}".format(i), auth=HTTPBasicAuth(user, password))
    return response


def calculate_avg_time_for_request_one_thread(req_number, path, user, password):
    avg_time = []
    for i in range(1, req_number+1, 1):
        start_time = datetime.datetime.now()
        response = send_request_without_prints(path, user, password, i)
        end_time = datetime.datetime.now()
        assert 200 <= response.status_code < 300
        avg_time.append(end_time.microsecond - start_time.microsecond)
    return sum(avg_time) / req_number

