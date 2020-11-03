import os
import sys

from playsound import playsound
from random import randrange
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities

from secrets import QC_EMAIL, QC_PASSWORD, QC_URL

MAX_RETRIES = 5


class NetflixQCBot:
    def __init__(self):
        print(' ' * 60, end='\r')
        print(' Initializing...', end='\r')
        capabilities = DesiredCapabilities.CHROME
        capabilities['pageLoadStrategy'] = 'eager'
        self.driver = webdriver.Chrome(desired_capabilities=capabilities)
        # self.driver.set_window_position(1150, 0)
        print(' ' * 60, end='\r')
        print(f' Accessing {QC_URL} ...', end='\r')
        self.driver.get(QC_URL)

    def login(self):
        print(' ' * 60, end='\r')
        print(' logging in ...', end='\r')
        sleep(2)
        email = self.driver.find_element_by_xpath('//*[@id="username"]')
        email.send_keys(QC_EMAIL)
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(QC_PASSWORD)
        sign_in = self.driver.find_element_by_xpath('//*[@id="post-ok"]/span')
        sign_in.click()

        self.click_pick_a_task()

    def click_pick_a_task(self):
        print(' ' * 60, end='\r')
        print(' Going to the picking tasks area ...', end='\r')
        sleep(3)
        pick_a_task = self.driver.find_element_by_xpath(
            '//*[@id="appContainer"]/div/div[2]/div/div[1]/div[2]/div/button'
        )
        pick_a_task.click()

    def get_if_exists_by_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return element

    def check_for_tasks(self):
        retries = 0
        found_tasks = False
        number_of_iterations = 0
        while not found_tasks:
            number_of_iterations += 1

            # wait between 0.9 and 3.5 seconds
            wait_time = randrange(9, 35) / 10

            print(' ' * 60, end='\r')
            print(
                (
                    f' (#{number_of_iterations}) Waiting for {wait_time} seconds '
                    'before checking again...'
                ),
                end='\r',
            )
            sleep(wait_time)

            print(' ' * 60, end='\r')
            print(f' (#{number_of_iterations}) checking for tasks', end='\r')

            check_for_tasks = self.get_if_exists_by_xpath(
                '//*[@id="appContainer"]/div/div[2]/div/div/div[2]/div[2]/button'
            )

            if check_for_tasks:
                check_for_tasks.click()
            elif retries < MAX_RETRIES:
                retries += 1
                print(' ' * 60, end='\r')
                print(
                    ' Cannot find the "Check for tasks button", retrying (#{retries}) ...',
                    end='\r',
                )
            else:
                print('#' * 30)
                print(
                    'Couldn\'t find the "Check for tasks" button :(\n'
                    'Please re-run the command  :)'
                )
                print('#' * 30)
                sys.exit(2)

            # wait for the reload, just for safety
            sleep(0.5)

            take_task = self.get_if_exists_by_xpath(
                '//*[@id="appContainer"]/div/div[2]/div/div/div[2]/div/div/div[2]'
                '/div[3]/button'
            )
            if take_task:
                print(' ' * 60, end='\r')
                print(' Hurray! Found tasks!!!')
                playsound('./sounds/three-beeps.mp3')
                found_tasks = True
                take_task.click()
            else:
                print(' ' * 60, end='\r')
                print(
                    f' (#{number_of_iterations}) No tasks found... trying again!',
                    end='\r',
                )

        agree_disclosure_pop_up = self.get_if_exists_by_xpath(
            '//*[@id="appContainer"]/div/div[2]/div/div/dialog/div/div/div/button[1]/span'
        )
        if agree_disclosure_pop_up:
            agree_disclosure_pop_up.click()


os.system('clear')
bot = NetflixQCBot()
bot.login()
bot.check_for_tasks()
