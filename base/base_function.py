from datetime import time

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

class Base(object):

    def __init__(self, driver, explicit_wait=45):
        """
        Inits Selenium Driver class with driver
        :param driver: WebDriver instance
        :param int explicit_wait: Time you want use as wait time
        :return A SeleniumDriver object

        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, explicit_wait)

    def driver(self):
        return self.driver

    def get_driver(self):
        """
        Get the web driver instance
        :rtype: WebDriver
        :return: WebDriver instance

        """
        driver = self.driver
        return driver


    def quit_driver(self):
        """
        Quit driver

        """

        self.driver.quit()


    def get_element(self, locator):
        """
        Get element for a provided locator
        :param locator: locator of the element to find
        :return: Element Object
        :rtype: WrapWebElement

        """
        try:
            element = self.driver.find_element(*locator)
        except (NoSuchElementException, StaleElementReferenceException):
            raise Exception("There is no such element or its" + str(locator) + " has changed ")
        return WrapWebElement(self.driver, element, locator)



class WrapWebElement(WebElement):
    """
    This class defines the generic interceptor for the methods of wrapped web element references.It also provides
    implementations for methods that acquire web element references

    """
    element = None
    driver = None
    locator = None

    def __init__(self, driver, element, locator=None):
        super().__init__(element.parent, element._id)
        self.element = element
        self.driver = driver
        self.locator = locator

    def find_element(self, *locator):
        """
        Find an element given a By strategy and locator.
        :param locator: locator of the element to find
        :rtype: WrapWebElement

        """
        if isinstance(locator[0], tuple):
            element = self.element.find_element(*locator[0])
            used_locator = locator[0]
        else:
            element = self.element.find_element(*locator)
            used_locator = locator
        return WrapWebElement(self.driver, element, locator=used_locator)

    def find_elements(self, *locator):
        """
        Find elements given locator.
        :param locator: locator of the elements to find
        :rtype: list of elements

        """
        if isinstance(locator[0], tuple):
            elements = self.element.find_elements(*locator[0])
            used_locator = locator[0]
        else:
            elements = self.element.find_elements(*locator)
            used_locator = locator
        return list(map(lambda el: WrapWebElement(self.driver, el, locator=used_locator), elements))

    def wait_visible(self, timeout=20):
        """
        Wait for element to be visible
        :param int timeout: Desired wait time before visibility of element
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda _: self.element.is_displayed(), "{} element not visible".format(str(self.locator)))
        return self

    def wait_enable(self, timeout=20):
        """
        Wait for element to be enable
        :param int timeout: Desired wait time before visibility of element
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda _: self.element.is_enabled(), "{} element not enable".format(str(self.locator)))
        return self

    def wait_clickable(self, timeout=20):
        """
        Wait for element to be clickable
        :param int timeout: Desired wait time before visibility of element
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        self.wait_visible(timeout=timeout)
        self.wait_enable(timeout=timeout)
        return self

    def click(self, delay=0):
        """
        Clicks the web element.
        :param float delay: Wait seconds before click
        :return: Desired visible element
        :rtype: WrapWebElement

        """
        if delay:
            time.sleep(delay)
        self.element.click()
        return self

    def js_click(self):
        """
        Clicks given element with execute script

        """
        self.driver.execute_script("arguments[0].click();", self.element)
        return self

    def double_click(self):
        """
        Double-clicks an element.
        :rtype: WrapWebElement

        """
        actions = ActionChains(self.driver)
        actions.double_click(self.element).perform()
        return self

    def right_click(self):
        """
        Right clicks an element.
        :rtype: WrapWebElement

        """
        actions = ActionChains(self.driver)
        actions.context_click(self.element).perform()
        return self

    def offset_click(self, x_offset, y_offset):
        """
         Function provides relative offset shifting
        :param x_offset: horizontal offset
        :param y_offset: vertical offset

        """
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.element, x_offset, y_offset)
        action.click()
        action.perform()
        return self

    def slide(self, x_offset, y_offset, no_element=False):
        """
        Slides an element by offsets
        :param x_offset: horizontal offset
        :param y_offset: vertical offset
        :param bool no_element: If True, clicks on current mouse position

        """
        action = ActionChains(self.driver)
        action.click_and_hold() if no_element else action.click_and_hold(self.element)
        action.move_by_offset(x_offset, y_offset)
        action.release()
        action.perform()
        return self

    def focus(self):
        """
        Focus on an an element.
        :rtype: WrapWebElement

        """
        actions = ActionChains(self.driver)
        actions.move_to_element(self.element).perform()
        self.click()
        return self

    def hover(self):
        """
        Hover to an element

        """
        actions = ActionChains(self.driver)
        actions.move_to_element(self.element).perform()
        return self

    def scroll(self, center=False):
        """
        Scrolls to an element
        :rtype: WrapWebElement

        """
        if center:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        else:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", self.element)
        return self

    def send_keys(self, value, delay=0):
        """
        Sends keys to current focused element.
        :param str value: A string for typing
        :param float delay: Requested wait time between typing each character
        :rtype: WrapWebElement

        """
        if delay:
            for char in list(value):
                self.element.send_keys(char)
                time.sleep(delay)
        else:
            self.element.send_keys(value)
        return self

    def action_chains_send_keys(self, *keys_to_send):
        """
        Sends keys to current focused element.
        :Args:
         - keys_to_send: The keys to send.  Modifier keys constants can be found in the
           'Keys' class.

        """
        actions = ActionChains(self.driver)
        actions.send_keys(*keys_to_send)
        actions.perform()

    def control_shortcuts(self, char):
        """
        Makes the desired shortcut operations with the control keys
        :param str char:  Give one of the shortcut letters

        """
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL)
        actions.key_down(char)
        actions.key_up(char)
        actions.key_up(Keys.CONTROL)
        actions.perform()

    def press_or_release_key(self, key_event="down", key_value=Keys.CONTROL):
        """
        Press or release given key, presses the control key by default
        :param str key_event: Button action up or down
        :param key_value: The key to press with 'Keys' class.

        """
        action = ActionChains(self.driver)
        if key_event == "down":
            action.key_down(key_value)
            action.perform()
        elif key_event == "up":
            action.key_up(key_value)
            action.perform()
        return self

    def __getattribute__(self, attribute):
        """
        Return getattr(self, name).
        :param str attribute: Attribute of the element
        :return: value of attribute

        """
        if attribute not in list(WrapWebElement.__dict__):
            returning_value = object.__getattribute__(self.element, attribute)
        else:
            returning_value = object.__getattribute__(self, attribute)

        def wrapper(*args, **kwargs):
            value = returning_value(*args, **kwargs)
            if (isinstance(value, WebElement) or attribute in (
                    "submit", "clear")) and attribute != 'find_element':
                return self
            else:
                return value

        if callable(returning_value):
            return wrapper
        else:
            return returning_value
