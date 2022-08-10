import time

from selenium import webdriver
from base.base_test import BaseTest
from page.home_page import HomePage
from page.careers_page import CareerPage

from base.base_function import Base
from selenium.webdriver.support import  expected_conditions as ec


class testCheckMoreButton(BaseTest):




     def webTestMoreButton(self):
        homepage=HomePage(self.driver)
        homepage.clickMoreButton()
        homepage.clickCareersButton()
        time.sleep(2)

        careerpage=CareerPage(self.driver)

     if __name__ == "__main__":
         BaseTest()
         webTestMoreButton()


     def tearDown(self):
         Base.quit_driver(self)



