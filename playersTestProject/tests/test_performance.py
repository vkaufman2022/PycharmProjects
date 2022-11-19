import concurrent.futures
import json
import datetime
import time

import requests
import helpers

config = json.load(open("appsettings.json"))
PATH = config["PATH"]
USER = config["USER"]
PASS = config["PASS"]
MAX_THREADS = 3
CONCURRENT_THREADS = 2


def test_1_request_one_thread():
    helpers.calculate_avg_time_for_request_one_thread(1,PATH,USER,PASS)
    print("Average time for 1 req: ", helpers.calculate_avg_time_for_request_one_thread(1,PATH,USER,PASS))


def test_10_request_one_thread():
    helpers.calculate_avg_time_for_request_one_thread(10,PATH,USER,PASS)
    print("Average time for 10 req: ", helpers.calculate_avg_time_for_request_one_thread(10,PATH,USER,PASS))


def test_50_request_one_thread():
    helpers.calculate_avg_time_for_request_one_thread(50,PATH,USER,PASS)
    print("Average time for 50 req: ", helpers.calculate_avg_time_for_request_one_thread(50,PATH,USER,PASS))


def test_100_request_one_thread():
    helpers.calculate_avg_time_for_request_one_thread(100,PATH,USER,PASS)
    print("Average time for 100 req: ", helpers.calculate_avg_time_for_request_one_thread(100,PATH,USER,PASS))


def test_multithreading_request():
    avg_time = []
    print ('Sending API request')
    response = helpers.send_request_without_prints(PATH, USER, PASS, 1)
    print ('Received: ', response.status_code, response.text)
    start_time = datetime.datetime.now()
    print ('Starting:', start_time)
    with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
        futures = [executor.submit(test_multithreading_request) for x in range (CONCURRENT_THREADS)]
    time.sleep(5)
    end_time = datetime.datetime.now()
    avg_time.append(end_time.microsecond - start_time.microsecond)
    print ('Average time:',sum(avg_time)/len(avg_time))