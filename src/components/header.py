from selenium.webdriver.common.by import By
from .base_component import BaseComponent

class Header(BaseComponent):
    EVENTS_LINK = (By.CSS_SELECTOR, "a[href*='/events']")
    ECO_NEWS_LINK = (By.CSS_SELECTOR, "a[href*='/news']")
    SIGN_UP_BTN = (By.CSS_SELECTOR, ".header_sign-up-btn")

    def click_events(self):
        self.find_element_in_component(self.EVENTS_LINK).click()

    def click_eco_news(self):
        self.find_element_in_component(self.ECO_NEWS_LINK).click()
