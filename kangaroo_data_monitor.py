from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os


class Monitor:
    def __init__(self):
        service = Service(executable_path="/Users/WilliamYu/Development/chromedriver")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.data_list = []

    def login(self, kan_mail, kan_password):
        # todo 1 build a webdriver
        self.driver.get(os.environ.get("login_page"))
        # todo 2 login the account
        email = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        button = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-hero-primary")))
        email.send_keys(kan_mail)
        password.send_keys(kan_password)
        button.click()
        # todo 3 check the data of each account
        data = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[class="font-w700"]')))
        self.data_list = data.text.strip().split()

    def check_data(self, threshold_value):
        used_data = self.data_list[:2]
        total_data = self.data_list[-2:]
        print(f"used data = {float(used_data[0])}{used_data[1]}, total data * threshold = {float(total_data[0]) * threshold_value}{total_data[1]}.")
        if used_data[1] == total_data[1] and float(total_data[0]) * threshold_value < float(used_data[0]):
            return True
        else:
            print("do not need to renew.\n")
            user_email_button = self.driver.find_element(By.ID, "page-header-user-dropdown")
            user_email_button.click()
            drop_down_button = self.driver.find_element(By.XPATH, '//*[@id="page-header"]/div/div[3]/div[2]/div/div/a[2]')
            drop_down_button.click()

            time.sleep(2)

            return False

    def renew_data(self):
        # todo 4 click for new data of account
        renew_button = self.driver.find_element(By.XPATH, '//*[@id="main-container"]/div/div[4]/div/div/div[2]/a[3]')
        renew_button.click()

        order_button = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cashier"]/div[2]/div[2]/button')))
        order_button.click()

        time.sleep(2)

        checkout_button = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cashier"]/div[2]/div/button')))
        checkout_button.click()
        print("********data renewed********.\n")
        self.driver.get(os.environ.get("main_page"))
