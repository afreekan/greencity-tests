from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_component import BaseComponent

class FilterPanel(BaseComponent):
    # Вибираємо
    LOCATION_SELECT = (By.XPATH, "//mat-select[api-select-title[contains(text(), 'Location')]]") # Adjusted based on common GreenCity structure
    # Якщо вище не вдається, використовуємо ID з subagent як резервну копію
    LOCATION_SELECT_ALT = (By.CSS_SELECTOR, "mat-select[formcontrolname='location']")
    
    STATUS_SELECT = (By.XPATH, "//mat-select[api-select-title[contains(text(), 'Status')]]")
    TYPE_SELECT = (By.XPATH, "//mat-select[api-select-title[contains(text(), 'Type')]]")
    
    OPTION_BY_TEXT = "//mat-option//span[contains(text(), '{text}')]"
    RESET_BUTTON = (By.XPATH, "//button[contains(text(), 'Reset all')]")

    def open_filter(self, filter_locator):
        # Використовуємо wait драйвера, оскільки mat-option часто з'являється поза контейнером компонента
        self._wait.until(EC.element_to_be_clickable(filter_locator)).click()

    def select_option(self, option_text):
        locator = (By.XPATH, self.OPTION_BY_TEXT.format(text=option_text))
        self._wait.until(EC.element_to_be_clickable(locator)).click()
        # Натискаємо поза межами, щоб закрити якщо він не закривається автоматично

    def filter_by_location(self, city):
        import time
        from selenium.common.exceptions import TimeoutException, NoSuchElementException

        # 1. Відкриваємо випадаючий список фільтра локації
        filter_triggers = self.driver.find_elements(By.XPATH, "//mat-select[.//mat-label[contains(., 'Location') or contains(., 'Локація') or contains(., 'Місто')]] | //mat-select[@formcontrolname='location'] | //mat-select[@id='mat-select-2']")
        if filter_triggers:
            try:
                self._wait.until(EC.element_to_be_clickable(filter_triggers[0])).click()
            except:
                self.driver.execute_script("arguments[0].click();", filter_triggers[0])
            self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "mat-option, .mat-mdc-option")))

        # 2. Перевіряємо, чи місто вже є в основному списку, і ставимо його
        options = self.driver.find_elements(By.XPATH, f"//mat-option//span[contains(text(), '{city}') or contains(text(), 'Київ')]")
        if options and options[0].is_displayed():
            try:
                options[0].click()
            except:
                self.driver.execute_script("arguments[0].click();", options[0])
            self.driver.execute_script("document.body.click();") 
            return

        # 3. Відкриваємо модальне вікно через 'Filter cities'
        try:
            filter_cities_btn = self._wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-mdc-select-panel button, .btn-filter-cities")))
            filter_cities_btn.click()
        except:
            self.driver.execute_script("""
            var btns = Array.from(document.querySelectorAll('.mat-mdc-select-panel button, .mat-select-panel button'));
            for(var b of btns) {
               if(b.innerText.toLowerCase().includes('filter') || b.innerText.toLowerCase().includes('фільтр')) { b.click(); return; }
            }
            """)
        
        # Чекаємо на загальне накладання модального вікна
        self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cdk-overlay-pane input, input[type='text'], input.mat-mdc-autocomplete-trigger")))

        # 4. Шукаємо в модальному вікні
        try:
            search_input = self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cdk-overlay-pane input, input[type='text'], input.mat-mdc-autocomplete-trigger")))
            search_input.send_keys(city)
        except:
            self.driver.execute_script(f"""
            var input = document.querySelector('.cdk-overlay-pane input');
            if(input) {{
                input.value = '{city}';
                input.dispatchEvent(new Event('input', {{bubbles: true}}));
            }}
            """)
            
        # Чекаємо на оновлення варіантів автозаповнення на основі введеного тексту
        try:
            self._wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "mat-option")) > 0)
        except:
            pass

        # 5. Вибираємо з автозаповнення
        try:
            auto_opts = self.driver.find_elements(By.CSS_SELECTOR, "mat-option")
            for opt in auto_opts:
                if city in opt.text or "Київ" in opt.text:
                    opt.click()
                    break
        except:
            pass

        # 6. Застосовуємо через save-cities-button
        try:
            save_btn = self._wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-cities-button, .cdk-overlay-pane button.mat-primary")))
            save_btn.click()
        except:
            self.driver.execute_script("var btn = document.querySelector('.save-cities-button'); if(btn) btn.click();")
        
        # Чекаємо, поки модальне вікно зникне
        try:
            self._wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".save-cities-button")))
        except:
            pass

        new_options = self.driver.find_elements(By.XPATH, f"//mat-option//span[contains(text(), '{city}') or contains(text(), 'Київ')]")
        if new_options:
            try:
                new_options[0].click()
            except:
                self.driver.execute_script("arguments[0].click();", new_options[0])

        try:
            self.driver.execute_script("document.body.click();")
        except:
            pass

    def reset_filters(self):
        try:
            btn = self.find_element_in_component(self.RESET_BUTTON)
            if btn.is_enabled():
                btn.click()
        except:
            pass
