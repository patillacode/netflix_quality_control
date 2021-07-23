import os

# from playsound import playsound
from fabulous import text
from random import randrange
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities

from secrets import QC_EMAIL, QC_PASSWORD, QC_URL


def print_banner():
    os.system('clear')
    try:
        print(text.Text("NeTQCBot", color='green', shadow=True, skew=3))
    except:
        print('NeTQCBot')
    print('\t\t\t\t\t\tby PatillaCode')


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
        sleep(5)

    def click_view_pool(self):
        view_pool = self.get_if_exists_by_xpath(
            '//*[@id="root"]/div/div/div[2]/div/div/button'
        )

        if view_pool:
            view_pool.click()
        else:
            print('Cannot find the "View Pool button"...')

    def close_modal(self):
        close_modal_button = self.get_if_exists_by_xpath(
            '/html/body/section/div/header/div/button'
        )

        if close_modal_button:
            close_modal_button.click()
        else:
            print('Cannot find the "X" button to close the modal')

    def task_not_available(self):
        return self.get_if_exists_by_xpath(
            '//*[text()="There are no tasks available currently in the SASS pool."]'
        )

    def take_task(self):
        print('#' * 45)
        print('\nTake the task, if there are no tasks restart!\n')
        print('#' * 45)

    def ping_pong(self):

        found = False
        number_of_iterations = 0

        while not found:
            number_of_iterations += 1

            sleep(randrange(10, 25) / 10)

            print(' ' * 60, end='\r')
            print(f' (#{number_of_iterations}) checking for tasks', end='\r')
            self.click_view_pool()

            sleep(randrange(10, 15) / 10)

            if self.get_if_exists_by_xpath(
                '//*[text()="There are no tasks available currently in the SASS pool."]'
            ):
                print(' ' * 60, end='\r')
                print(
                    ' No tasks found... trying again!',
                    end='\r',
                )
                sleep(randrange(10, 15) / 10)
                self.close_modal()
            else:
                found = True
                self.take_task()

    def get_if_exists_by_xpath(self, xpath):
        try:
            return self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False


if __name__ == '__main__':
    print_banner()
    bot = NetflixQCBot()
    bot.login()
    bot.ping_pong()
