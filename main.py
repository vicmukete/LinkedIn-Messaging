import csv
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, \
    ElementClickInterceptedException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys

driver_path = r"C:\Users\muket\Desktop\Chrome Drivers\chromedriver.exe"

driver_option = webdriver.ChromeOptions()


# driver_option.add_argument('--incognito')

# df = pd.read_csv('LinkedIn Stats')

# login function
def login_info(driver, email, password):
    email_login = driver.find_element(By.ID, 'username')
    email_login.click()
    email_login.send_keys(email)
    password_login = driver.find_element(By.ID, 'password')
    password_login.click()
    password_login.send_keys(password)
    password_login.send_keys(Keys.RETURN)


# initialize webdriver
def create_wb():
    service = Service(driver_path)
    driver_option.add_argument('--start maximized')
    return webdriver.Chrome(service=service, options=driver_option)


# terms to avoid
def avoid_these_names():
    key_words = []
    while True:
        names_to_avoid = input("Are there any specific names/words you'd like to avoid? (y or n): ").lower()
        if names_to_avoid == 'y':
            key_word = input("Enter key words to avoid: ")
            print()
            key_words.append(key_word)
            print(key_words)
        elif names_to_avoid == 'n':
            print('Ok :)')
            return


def create_csv(profile_data=None):
    numOfData = 12
    file_exist = os.path.isfile('LinkedIn Stats')

    if profile_data is not None:
        data_write = profile_data

        if len(data_write) < numOfData:
            data_write += ['N/A'] * (numOfData - len(data_write))

        with open("LinkedIn Stats", 'a', newline="") as csv_file:
            write = csv.writer(csv_file)
            if not file_exist:
                write.writerow([])
            write.writerow(data_write)


def main():
    # primary information
    search = 'data science'
    email = 'muketevictor6@gmail.com'
    password = 'DiboNtina80'
    print()
    # search = input('What jobs would you like to search for: ')
    # email = input('Enter LinkedIn email: ')
    # password = input('Enter LinkedIn Password: ')

    # login process
    driver = create_wb()
    driver.get(f'https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage'
               f'-basic_nav-header-signin')
    login_info(driver, email, password)

    # search process
    try:
        WebDriverWait(driver, 2).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="global-nav-typeahead"]'))
        )
        search_box = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]')
        search_box.click()
        time.sleep(5)
        search_box.send_keys(search)
        search_box.send_keys(Keys.RETURN)

    except TimeoutException:
        print('Timeout, waiting for search box to load')
    except (ElementNotInteractableException, ElementClickInterceptedException):
        print('Error interacting with search box')

    driver.quit()


main()
