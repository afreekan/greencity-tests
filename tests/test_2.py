import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestGreenCityEvents(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.greencity.cx.ua/#/greenCity/events")

    def tearDown(self):
        self.driver.quit()

    def test_filter_by_location_kyiv(self):

        # Натиснути на панель фільтрів у блоці "Location"
        location_panel = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@class, 'filter-container')]//*[contains(text(), 'Location') or contains(text(), 'Локація')]")
        ))
        location_panel.click()
        
        # Натиснути кнопку «Filter cities» у випадному меню
        filter_cities_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@class, 'cdk-overlay-pane')]//*[contains(text(), 'Filter cities')]")
        ))
        filter_cities_button.click()

        #Ввести "Kyiv" у модальному вікні та вибрати перший результат
        location_input_field = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'cdk-overlay-pane')]//input")
        ))
        
        location_input_field.click()
        location_input_field.clear()
        location_input_field.send_keys("Kyiv")
        
        # Вибір першого результату із випадаючого списку
        first_suggestion = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[contains(@class, 'cdk-overlay-pane')]//span[contains(text(), 'Kyiv')])[1]")
        ))
        first_suggestion.click()
        
        # Натискання кнопки "Add selected cities" для підтвердження
        add_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Add selected cities')]")
        ))
        add_button.click()

        # Вибір доданого міста в основному списку фільтрів
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
        
        # Перевіряємо, чи видно чекбокс
        try:
            kyiv_option = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//mat-option[.//span[contains(text(), 'Kyiv')]]")
            ))
        except:
            location_panel.click()
            kyiv_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//mat-option[.//span[contains(text(), 'Kyiv')]]")
            ))

        kyiv_option.click()
        
        # Закриваємо меню фільтрів
        self.driver.execute_script("document.querySelector('.cdk-overlay-backdrop').click();")

        # Перевірити локацію у всіх знайдених картках подій
        # 1. Очікуємо, поки з'явиться хоча б одна картка
        location_xpath = "//span[@class='place']/following-sibling::p"
        self.wait.until(EC.presence_of_element_located((By.XPATH, location_xpath)))

        # 2. Знаходимо ВСІ елементи з адресами на сторінці
        event_locations = self.driver.find_elements(By.XPATH, location_xpath)
        
        # 3. Перевіряємо кількість
        self.assertGreater(len(event_locations), 0, "Після фільтрації список подій порожній")
        
        print(f"DEBUG: Перевіряємо {len(event_locations)} карток...")

        # 4. Проходимо циклом по кожній картці
        for loc in event_locations:
            actual_text = loc.text
            print(f"DEBUG: Текст у коді картки: {actual_text}")
if __name__ == "__main__":
    unittest.main()