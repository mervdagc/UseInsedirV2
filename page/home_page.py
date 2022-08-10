import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import  expected_conditions as ec

class HomePage():
    more_button=(By.XPATH,"//body[1]/nav[1]/div[2]/div[1]/ul[1]/li[6]/a[1]/span[1]")
    careers_button = (By.XPATH, "//body/nav[@id='navigation']/div[2]/div[1]/ul[1]/li[6]/div[1]/div[1]/div[3]/div[1]/a[1]")



    def __init__(self,driver,explicit_wait=45):
        self.driver=driver
        self.wait=WebDriverWait(self.driver,explicit_wait)

    def check(self):
        self.wait.until(ec.visibility_of_element_located(self.more_button), "Login page isn't visible!")
        self.wait.until(ec.visibility_of_element_located(self.careers_button), "Login page isn't visible!")

    def clickMoreButton(self):
        self.wait.until(ec.element_to_be_clickable(self.more_button),"Bulunamadı").click()

    def clickCareersButton(self):
        self.wait.until(ec.element_to_be_clickable(self.careers_button), "Bulunamadı").click()




        time.sleep(3)