import os
import sys
import random

from secrets import QC_EMAIL, QC_PASSWORD, QC_REQUEST_TASKS_URL, QC_TAKE_TASK_URL, QC_URL
from time import sleep

import requests

from gif_for_cli import execute
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from yaspin import kbi_safe_yaspin
from yaspin.spinners import Spinners


def login_and_get_cookie(driver, spinner):
    # capabilities = DesiredCapabilities.CHROME
    # capabilities['pageLoadStrategy'] = 'eager'
    # driver = webdriver.Chrome(desired_capabilities=capabilities)
    # driver.set_window_position(1150, 0)
    spinner.text = f'Accessing {QC_URL} ...'
    driver.get(QC_URL)
    sleep(3)
    email_input = driver.find_element(by=By.XPATH, value='//*[@id="user-identifier"]')
    email_input.send_keys(QC_EMAIL)
    sleep(1)
    continue_button = driver.find_element(by=By.XPATH, value='//*[@id="btn-continue"]')
    continue_button.click()

    spinner.text = 'Second step, entering password ...'
    sleep(3)
    password = driver.find_element(by=By.XPATH, value='//*[@id="field-password"]')
    password.send_keys(QC_PASSWORD)
    sleep(1)
    spinner.text = 'Logging in...'
    login_button = driver.find_element(by=By.XPATH, value='//*[@id="btn-login"]')
    login_button.click()
    sleep(3)
    cookie = driver.get_cookie('wall-e_auth_openidc_session')
    driver.close()
    return cookie


def get_task(session, cookie, data, spinner):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'content-length': '1031',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': (f'wall-e_auth_openidc_session={cookie["value"]}'),
        'origin': 'https://assetqc.netflixstudios.com',
        'referer': 'https://assetqc.netflixstudios.com/my-tasks',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
        ),
    }

    payload = {
        "details": {},
        "presentedQcTasks": [data['qcTasks'][0]],
        "selectedQcTaskIds": [data['qcTasks'][0]['qcTaskId']],
        "user": QC_EMAIL,
    }

    spinner.text = 'Getting a task!'

    response = session.post(QC_TAKE_TASK_URL, json=payload, headers=headers)
    if response.status_code != 200:
        spinner.text = 'Task is no longer available, looking for more...'
        sleep(3)
        return False

    spinner.text = 'Got it!'
    spinner.stop()
    gif()
    return True


def gif():
    random_gif = random.choice(os.listdir('./gifs/'))
    execute.execute(os.environ, [f'./gifs/{random_gif}'], sys.stdout)


def request_available_tasks(session, cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en;q=0.9',
        'cookie': f'wall-e_auth_openidc_session={cookie["value"]}',
        'referer': 'https://assetqc.netflixstudios.com/my-tasks',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    }
    response = session.get(QC_REQUEST_TASKS_URL, headers=headers)

    if response.status_code != 200:
        print(f'\n Something went wrong, please restart [{response.status_code}]')
        return False
    return response.json()


def get_random_spinner():
    spinner_choices = [
        Spinners.aesthetic,
        Spinners.pong,
        Spinners.dots2,
        Spinners.bouncingBar,
        Spinners.bouncingBall,
    ]
    color_choices = ['magenta', 'green', 'yellow', 'white']
    return kbi_safe_yaspin(
        random.choice(spinner_choices),
        color=random.choice(color_choices),
        side='left',
        reversal=True,
        timer=True,
    )


def main():
    spinner = get_random_spinner()
    spinner.start()
    spinner.text = 'Initializing...'

    capabilities = DesiredCapabilities.CHROME
    capabilities['pageLoadStrategy'] = 'eager'
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    cookie = login_and_get_cookie(driver, spinner)

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as session:
        found_task = False
        iteration = 0

        while not found_task:
            iteration += 1
            json_response = request_available_tasks(session, cookie)

            if json_response['qcTasks']:
                found_task = get_task(session, cookie, json_response, spinner)
            else:
                wait_time = random.randrange(10, 25) / 10
                spinner.text = (
                    f'(#{iteration}) Nothing yet... trying again in {wait_time} seconds'
                )
                sleep(wait_time)


if __name__ == '__main__':
    main()
