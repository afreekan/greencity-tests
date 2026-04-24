from selenium.webdriver.common.by import By
from .base_component import BaseComponent

class EventCard(BaseComponent):
    TITLE = (By.CSS_SELECTOR, ".title, .event-title, h4, h3, .name")
    DATE = (By.CSS_SELECTOR, ".date, .event-date, .time")
    LOCATION = (By.CSS_SELECTOR, ".location span, .address, .event-location-text, .location")
    TAGS = (By.CSS_SELECTOR, "a.tag")

    @property
    def title(self):
        from selenium.common.exceptions import NoSuchElementException
        try:
            return self.find_element_in_component(self.TITLE).get_attribute("textContent").strip()
        except NoSuchElementException:
            return ""

    @property
    def date(self):
        from selenium.common.exceptions import NoSuchElementException
        try:
            return self.find_element_in_component(self.DATE).get_attribute("textContent").strip()
        except NoSuchElementException:
            return ""

    @property
    def location(self):
        locators = [
            (By.XPATH, ".//span[contains(@class, 'place')]/following-sibling::p"),
            (By.CSS_SELECTOR, ".date-container p"),
            (By.XPATH, ".//div[contains(@class, 'date-container')]//p[contains(text(), 'Kyiv') or contains(text(), 'Київ') or contains(text(), 'Online') or contains(text(), 'Онлайн')]")
        ]
        
        for selector, path in locators:
            try:
                # Шукаємо саме з контейнера картки
                element = self.container.find_element(selector, path)
                text = element.get_attribute("textContent")
                if text and text.strip():
                    return text.strip()
            except:
                continue
        return ""

    def click(self):
        self.container.click()

    def get_tags(self):
        elements = self.find_elements_in_component(self.TAGS)
        return [el.text for el in elements]
