import time
import unittest


from selenium import webdriver
from base.base_function import Base


class BaseTest():


    def __init__(self):
        self.driver = webdriver.Chrome("/Users/mrvdgc/PycharmProjects/UseInsedirV2/base/webdrivers/chromedriverMac64")
        self.driver.get("https://useinsider.com/")
        self.driver.maximize_window()

        time.sleep(2)

    def drivertest(self):
        time.sleep(2)

