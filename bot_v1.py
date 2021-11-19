import os
import sys
import random

from secrets import QC_EMAIL, QC_PASSWORD, QC_REQUEST_TASKS_URL, QC_TAKE_TASK_URL, QC_URL
from time import sleep

import requests

from gif_for_cli import execute
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from yaspin import kbi_safe_yaspin
from yaspin.spinners import Spinners


def get_form_action_and_cookie(spinner):
    spinner.text = 'Initializing...'
    capabilities = DesiredCapabilities.CHROME
    capabilities['pageLoadStrategy'] = 'eager'
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    # driver.set_window_position(1150, 0)
    spinner.text = f'Accessing {QC_URL} ...'
    driver.get(QC_URL)
    sleep(3)

    spinner.text = 'Getting login URL...'
    form_action = driver.find_element_by_xpath('/html/body/div/div/form').get_attribute(
        'action'
    )
    sleep(2)

    spinner.text = 'Getting cookie...'
    cookie = driver.get_cookie('PF')
    driver.close()

    return form_action, cookie


def get_task(session, data, spinner):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'content-length': '1031',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': (
            'wall-e_auth_openidc_session='
            f'{session.cookies.get_dict()["wall-e_auth_openidc_session"]}'
        ),
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


def get_login_payload_and_headers(cookie):
    headers = {
        'Host': 'meechum.netflix.com',
        'Connection': 'keep-alive',
        # 'Content-Length': '139',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://meechum.netflix.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
            'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        ),
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://meechum.netflix.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cookie': f'{cookie["name"]}={cookie["value"]}',
    }
    payload = {
        'pf.username': QC_EMAIL,
        'pf.pass': QC_PASSWORD,
        'pf.ok': 'clicked',
        'pf.cancel': '',
        'pf.adapterId': 'nflxPartnerDirectoryLogin',
        'pf.alternateAuthnSystem': '',
    }

    return payload, headers


def request_available_tasks(session):
    response = session.get(QC_REQUEST_TASKS_URL)

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

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as session:
        form_action_url, cookie = get_form_action_and_cookie(spinner)
        payload, headers = get_login_payload_and_headers(cookie)
        session.post(form_action_url, data=payload, headers=headers)

        found_task = False
        iteration = 0

        while not found_task:
            iteration += 1
            json_response = request_available_tasks(session)

            if json_response['qcTasks']:
                found_task = get_task(session, json_response, spinner)
            else:
                wait_time = random.randrange(10, 25) / 10
                spinner.text = (
                    f'(#{iteration}) Nothing yet... trying again in {wait_time} seconds'
                )
                sleep(wait_time)


if __name__ == '__main__':
    main()
