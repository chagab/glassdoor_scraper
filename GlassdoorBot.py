from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep


class GlassdoorBot():

    short_sleep_time = 3
    long_sleep_time = 10
    _current_location = ''
    _current_jobTitle = ''
    _current_salary = ''

    def __init__(self, email, password, headless=True) -> None:
        self.email = email
        self.password = password
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.random
        if headless:
            options.add_argument("--headless=new")
        else:
            options.add_argument("start-maximized")
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        print(self.driver.execute_script("return navigator.userAgent;"))

    def open_glassdoor(self) -> None:

        self.driver.get('https://www.glassdoor.com/index.htm')

        try:
            login_button = WebDriverWait(self.driver, self.long_sleep_time).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/header/div/div/div[2]/div/button")
                )
            )
            login_button.click()

        except ElementClickInterceptedException:
            # get rid of the Google Login popup
            google_login_popup_close = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'close'))
            )
            google_login_popup_close.click()
            login_button.click()

        self.email_login()

    def email_login(self) -> None:
        inputMail = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located(
                (By.ID, "modalUserEmail")
            )
        )
        inputMail.send_keys(self.email)
        inputMail.send_keys(Keys.RETURN)

        inputPassword = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located(
                (By.ID, "modalUserPassword")
            )
        )
        inputPassword.send_keys(self.password)
        inputPassword.send_keys(Keys.RETURN)

    def open_salaries(self) -> None:
        sleep(self.short_sleep_time)
        salaries_button = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/header/div/div/ul/li[4]/a")
            )
        )
        salaries_button.click()

    def input_job_title(self, job_title) -> None:
        self._current_jobTitle = job_title
        inputJobTitle = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[id^=typedKeyword]")
            )
        )
        inputJobTitle.send_keys(job_title)

    def input_location(self, location) -> None:
        self._current_location = location
        inputlocation = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[id^=Autocomplete]")
            )
        )
        inputlocation.send_keys(location)
        sleep(self.short_sleep_time)
        inputlocation.send_keys(Keys.DOWN)
        inputlocation.send_keys(Keys.ENTER)
        inputlocation.send_keys(Keys.ENTER)

    def scrape_salary_details(self) -> None:
        big_ass_xpath = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/" \
            + "div[2]/div[3]/div[1]/div[1]/div"
        sleep(self.short_sleep_time)
        total_pay_range = WebDriverWait(self.driver, self.long_sleep_time).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    big_ass_xpath
                )
            )
        )
        self._current_salary = total_pay_range.text

        return (
            self._current_jobTitle,
            self._current_location,
            self._current_salary
        )

    def get_salary_details(self, jobTitle, location) -> None:
        self.open_salaries()
        self.input_job_title(jobTitle)
        self.input_location(location)
        return self.scrape_salary_details()
