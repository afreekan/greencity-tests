import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestEventsPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.greencity.cx.ua/#/greenCity/events")

    def tearDown(self):
        self.driver.quit()

    # Test Case 1: Перевірка відображення детальної інформації про обрану подію
    def test_view_existing_event_details(self):
        # Крок 1: Знайти картку події та клікнути на неї
        card_locator = (By.CSS_SELECTOR, "mat-card.event-list-item .secondary-global-button")
        
        first_event_card = self.wait.until(EC.element_to_be_clickable(card_locator))
        first_event_card.click()

        # Крок 2: Перевірити наявність основних елементів
        back_button_locator = (By.CSS_SELECTOR, "a.button-link") # Кнопка "Back to events"
        title_locator = (By.CSS_SELECTOR, "div.event-title") # Заголовок події
        
        back_btn = self.wait.until(EC.visibility_of_element_located(back_button_locator))
        event_title = self.wait.until(EC.visibility_of_element_located(title_locator))
        
        self.assertTrue(event_title.is_displayed(), "Заголовок детальної сторінки не відображається")
        self.assertTrue(back_btn.is_displayed(), "Кнопка 'Back to events' не відображається")

        # Крок 3: Натиснути кнопку "Back to events"
        back_btn.click()

        # Перевірка
        self.wait.until(EC.url_contains("greenCity/events"))
        self.assertIn("events", self.driver.current_url, "Не вдалося повернутися на сторінку списку подій")


if __name__ == "__main__":
    unittest.main()
