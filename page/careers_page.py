import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from base.base_function import *
from selenium.webdriver.support import expected_conditions as ec


class CareerPage():
    careers_button = (By.XPATH, "//body/nav[@id='navigation']/div[2]/div[1]/ul[1]/li[6]/div[1]/div[1]/div[3]/div[1]/a[1]")
    LOCATION_FIELDS = (By.XPATH, "//input[contains(@class, 'location')]")



    def __init__(self,driver,explicit_wait=45):
        self.driver=driver
        self.wait=WebDriverWait(self.driver,explicit_wait)

    def check(self):
        self.wait.until(ec.visibility_of_element_located(self.more_button), "Login page isn't visible!")
        self.wait.until(ec.visibility_of_element_located(self.careers_button), "Login page isn't visible!")




