from selenium.webdriver.support.ui import WebDriverWait

class BaseComponent:
    def __init__(self, driver, container):
        self.driver = driver
        self.container = container
        self._wait = WebDriverWait(driver, 10)

    def find_element_in_component(self, locator):
        # Знаходить елемент ТІЛЬКИ всередині контейнера компонента.
        return self.container.find_element(*locator)

    def find_elements_in_component(self, locator):
        # Знаходить усі елементи ТІЛЬКИ всередині контейнера компонента.
        return self.container.find_elements(*locator)
