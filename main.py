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


def splitting_search(search):
    if ' ' in search:
        search = search.split()
        return search


# initialize webdriver
def create_wb():
    service = Service(driver_path)
    driver_option.add_argument('--start maximized')
    driver_option.add_argument('--disable-notifications')
    return webdriver.Chrome(service=service, options=driver_option)


# terms to avoid
def avoid_these_names():
    key_words = []
    while True:
        names_to_avoid = input("Are there any specific names/words you'd like to avoid? (y or n): ").lower()
        if names_to_avoid == 'y':
            key_word = input("Enter key words to avoid: \n")
            key_words.append(key_word)
            print(key_words)
        elif names_to_avoid == 'n':
            print('Ok :)')
            return


def create_csv(profile_data=None):
    numOfData = 5
    file_exist = os.path.isfile('LinkedIn Stats')

    if profile_data is not None:
        data_write = profile_data

        if len(data_write) < numOfData:
            data_write += ['N/A'] * (numOfData - len(data_write))

        with open("LinkedIn Stats", 'a', newline="") as csv_file:
            write = csv.writer(csv_file)
            if not file_exist:
                write.writerow(['Name', 'Position', 'Company', 'Alma Mater', 'Experience'])
            write.writerow(data_write)


def scraped_data(driver, num):
    scraped_names = []
    scraped_job = []
    scraped_company = []
    scraped_alma_mater = []
    # for index in range(0, num):
    # loop may be in the wrong place
    try:
        WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.TAG_NAME, 'button'))
        )
        all_buttons = driver.find_element(By.TAG_NAME, 'button')
        connect_buttons = [btn for btn in all_buttons if btn.text() == 'Connect']
        connect_buttons[0].click()
    except TimeoutException:
        print('Timeout, waiting for element to load.')

    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException,
            WebDriverException):
        print('Error interacting with element.')


    '''job = driver.find_element(By.CLASS_NAME, 'text-body-medium break-words').text  # also had profile-content XPATH
    company = driver.find_element(By.XPATH, '//*[@id="profile-content"]').text
    alma_mater = driver.find_element(By.XPATH, '//*[@id="profile-content"]').text
    scraped_names.append(name)
    scraped_job.append(job)
    scraped_company.append(company)
    scraped_alma_mater.append(alma_mater)'''


def main():
    # login process
    # primary information
    search = 'data science recruiter'
    email = 'muketevictor6@gmail.com'
    password = 'DiboNtina80'
    num = 2
    print()
    # search = input('What jobs would you like to search for: ')
    # email = input('Enter LinkedIn email: ')
    # password = input('Enter LinkedIn Password: ')
    '''try:
        num = int(input('How many companies do you want scraped: '))
    except SyntaxError:
        print('Please enter a valid integer')'''

    var = splitting_search(search)

    # handles <= 3 word searches
    driver = create_wb()

    if len(var) >= 3:
        driver.get(
            f'https://www.linkedin.com/search/results/all/?keywords={var[0]}%20{var[1]}%20{var[2]}&origin'
            f'=GLOBAL_SEARCH_HEADER&sid=So%40')
        login_info(driver, email, password)

    elif len(var) == 2:
        driver.get(
            f'https://www.linkedin.com/search/results/all/?keywords={var[0]}%20{var[1]}&origin=GLOBAL_SEARCH_HEADER'
            f'&sid=css')
        login_info(driver, email, password)

    else:
        driver.get(f'https://www.linkedin.com/search/results/all/?keywords={var}&origin=GLOBAL_SEARCH_HEADER&sid=Jm6')
        login_info(driver, email, password)

    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CLASS_NAME, 'artdeco-pill--choice'))
    )
    list_button_ppl = driver.find_element(By.CLASS_NAME, 'artdeco-pill--choice')
    list_button_ppl.click()
    time.sleep(10)
    scraped_data(driver, num)

    driver.quit()

    # search process


'''    try:
        WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="global-nav-typeahead"]'))
        )
        search_bar = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]')
        search_bar.click()
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.RETURN)

    except TimeoutException:
        print('Timeout, waiting for search box to load')
    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException,
            WebDriverException):
        print('Error interacting with search box')

    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="search-reusables__filters-bar"]'))
    )
    list_button_ppl = driver.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]')
    list_button_ppl.click()

    driver.quit()'''

main()
