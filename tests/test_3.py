import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestEventsPage(unittest.TestCase):

    def setUp(self):
        print("\nЗапуск браузера...")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get("https://www.greencity.cx.ua/#/greenCity/events")

    def tearDown(self):
        print("Закриття браузера")
        self.driver.quit()

    def test_toggle_view_modes(self):
        print("--- СТАРТ ТЕСТУ ---")

        # Чекаємо завантаження карток
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'event-list')]")))

        # Локатори кнопок
        grid_btn_xpath = "//*[contains(@class, 'gallery')]"
        list_btn_xpath = "//*[contains(@class, 'nav-left-list')]"

        grid_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, grid_btn_xpath)))
        list_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, list_btn_xpath)))

        print("Перевірка, що Grid відображається...")
        self.assertTrue(grid_btn.is_displayed(), "Іконка Grid не відображається")

        # ПЕРЕМИКАННЯ НА LIST
        print("Натискання на 'List view'")
        self.driver.execute_script("arguments[0].click();", list_btn)

        print("Очікування зміни відображення на список")
        
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'list-view')]")))
        
        print("Режим 'List' активовано.")

        # ПЕРЕМИКАННЯ НА GRID
        print("Повернення до 'Grid view'...")
        self.driver.execute_script("arguments[0].click();", grid_btn)

        # Чекаємо поки клас list-view ЗНИКНЕ
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(@class, 'list-view-container')]")))
        
        # перевірка
        is_gallery_visible = self.driver.find_element(By.XPATH, "//*[contains(@class, 'gallery') or contains(@class, 'event-list')]").is_displayed()
        
        self.assertTrue(is_gallery_visible, "Відображення не повернулося до Grid")
        print("Тест завершено успішно!")

if __name__ == "__main__":
    unittest.main()