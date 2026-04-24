from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(driver, 15)

    def find_element(self, locator):
        return self._wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        from selenium.common.exceptions import TimeoutException
        try:
            return self._wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click(self, locator):
        element = self._wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def get_text_safe(self, locator):
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        try:
            return self.get_text(locator)
        except (TimeoutException, NoSuchElementException):
            return ""

    def is_visible_safe(self, locator):
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        try:
            return self.find_element(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_visibility(self, locator):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
