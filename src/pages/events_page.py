from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..components.header import Header
from ..components.filter_panel import FilterPanel
from ..components.event_card import EventCard

class EventsPage(BasePage):
    URL = "https://www.greencity.cx.ua/#/greenCity/events"
    
    # Locators
    GRID_VIEW_BTN = (By.CSS_SELECTOR, "button.gallery")
    LIST_VIEW_BTN = (By.CSS_SELECTOR, "button.list")
    EVENT_CARD_CONTAINER = (By.CSS_SELECTOR, "app-events-list-item")
    BACK_TO_EVENTS_BTN = (By.CSS_SELECTOR, "div.back-button, a[href*='/events']") # For event details page return
    
    # Detail Page Locators
    DETAIL_TITLE = (By.CSS_SELECTOR, "h1, .event-title, .title-name, .title")
    DETAIL_DATE = (By.CSS_SELECTOR, ".date-container, .event-date, .date")
    DETAIL_LOCATION = (By.CSS_SELECTOR, ".location, .address-container, .address")
    DETAIL_DESCRIPTION = (By.CSS_SELECTOR, ".description, .event-text, .text")
    DETAIL_IMAGE = (By.CSS_SELECTOR, "img.event-image, .event-image img, img.image")
    
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def header(self):
        return Header(self.driver, self.find_element((By.CSS_SELECTOR, "header, .header")))

    @property
    def filter_panel(self):
        return FilterPanel(self.driver, self.find_element((By.CSS_SELECTOR, ".filter-container, .fields-container")))

    def open(self):
        self.driver.get(self.URL)
        return self

    def get_all_event_cards(self):
        elements = self.find_elements(self.EVENT_CARD_CONTAINER)
        return [EventCard(self.driver, el) for el in elements]

    def switch_to_grid_view(self):
        self.click(self.GRID_VIEW_BTN)

    def switch_to_list_view(self):
        self.click(self.LIST_VIEW_BTN)

    def is_grid_view_active(self):
        btn = self.find_element(self.GRID_VIEW_BTN)
        classes = btn.get_attribute("class") or ""
        disabled = btn.get_attribute("disabled")
        return "active" in classes or "selected" in classes or disabled == "true" or disabled

    def is_list_view_active(self):
        btn = self.find_element(self.LIST_VIEW_BTN)
        classes = btn.get_attribute("class") or ""
        disabled = btn.get_attribute("disabled")
        return "active" in classes or "selected" in classes or disabled == "true" or disabled

    def click_back_to_events(self):
        self.click(self.BACK_TO_EVENTS_BTN)

    def get_details(self):
        return {
            "title": self.get_text_safe(self.DETAIL_TITLE),
            "date": self.get_text_safe(self.DETAIL_DATE),
            "location": self.get_text_safe(self.DETAIL_LOCATION),
            "description": self.get_text_safe(self.DETAIL_DESCRIPTION),
            "image_visible": self.is_visible_safe(self.DETAIL_IMAGE)
        }
