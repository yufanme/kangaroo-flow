from kangaroo_data_monitor import Monitor
import os
from datetime import datetime
import time
import random

MAIL_5629 = os.environ.get("MAIL_5629")
MAIL_1649 = os.environ.get("MAIL_1649")
MAIL_9527 = os.environ.get("MAIL_9527")
PASSWORD = os.environ.get("PASSWORD")
DATA_THRESHOLD_VALUE = 0.8
RUN_TIME_INTERVAL = 15
RANDOM_SECOND = random.randint(-100, 100)


def run_monitor():
    monitor = Monitor()
    emails = [MAIL_5629, MAIL_1649, MAIL_9527]
    for email in emails:
        print(email)
        monitor.login(email, PASSWORD)
        if monitor.check_data(DATA_THRESHOLD_VALUE):
            monitor.renew_data()
    monitor.driver.quit()


loop_time = 0
while True:
    print("--------------------------------------------------------------------")
    print(f"loop time: {loop_time}.")
    print(datetime.now())
    run_monitor()
    loop_time += 1
    print("--------------------------------------------------------------------  ")
    time.sleep(RUN_TIME_INTERVAL * 60 + RANDOM_SECOND)


