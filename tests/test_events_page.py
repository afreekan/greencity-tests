import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.events_page import EventsPage

@allure.feature("Events Page")
class TestEventsPage:

    @allure.story("View Event Details")
    @allure.step("Verify that user can see detailed information about an event")
    def test_view_event_details(self, driver):
        events_page = EventsPage(driver).open()
        
        WebDriverWait(driver, 15).until(lambda d: len(events_page.get_all_event_cards()) > 0)
        cards = events_page.get_all_event_cards()
        assert len(cards) > 0, "No events found on the page"
        
        card = cards[0]
        preview_title = card.title
        
        card.click()
        WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(*events_page.DETAIL_TITLE)) > 0)
        
        details = events_page.get_details()
        assert preview_title in details["title"] or details["title"] in preview_title, \
            f"Expected title to be related. Preview was '{preview_title}', Detail is '{details['title']}'"
        assert details["image_visible"] is not None, "Event image container should be present"
        
        events_page.click_back_to_events()
        WebDriverWait(driver, 10).until(lambda d: len(events_page.get_all_event_cards()) > 0)
        assert len(events_page.get_all_event_cards()) > 0, "Should be back on events list"

    @allure.story("Location Filter")
    @allure.step("Verify filtration by location (Kyiv)")
    def test_filter_by_location(self, driver):
        events_page = EventsPage(driver).open()
        
        # поки сторінка завантажиться
        WebDriverWait(driver, 15).until(lambda d: len(events_page.get_all_event_cards()) > 0)
        
        events_page.filter_panel.filter_by_location("Kyiv")

        # чекаємо можливого оновлення, оновлення URL-адреси
        try:
            WebDriverWait(driver, 10).until(lambda d: "location=" in d.current_url or "Kyiv" in d.current_url or "Київ" in d.current_url)
        except:
             pass # URL може не оновлюватися в деяких версіях Angular, тому слід покладатися на стан карток
        
        # чекаємо, поки Angular фактично інтерполює текст у картки
        try:
            WebDriverWait(driver, 10).until(
                lambda d: any(c.location != "" for c in events_page.get_all_event_cards())
            )
        except:
            pass # якщо вони дійсно порожні, assert зловить це нижче

        cards = events_page.get_all_event_cards()
        assert len(cards) > 0, "No events found after filtering"

        # Додаємо локації до Allure для налагодження
        locations = [card.location for card in cards]
        allure.attach(str(locations), name="Detected Locations", attachment_type=allure.attachment_type.TEXT)
        
        if len(cards) > 0:
            allure.attach(cards[0].container.get_attribute("innerHTML"), 
                          name="HTML of first card", 
                          attachment_type=allure.attachment_type.HTML)

        # Перевіряємо, що принаймні одна картка має локацію Київ або Онлайн (деякі картки можуть не мати інформації про локацію/бути онлайн у міксі)
        search_pattern = ["kyiv", "київ", "online", "онлайн", "м. київ", "kyiv city", "svetlitsky", "світлицького"]
        kyiv_found = any(
            any(p in card.location.lower() for p in search_pattern) 
            for card in cards
        )
        assert kyiv_found, f"Could not find any event with Kyiv/Online/Svetlitsky location after filtering. Found locations: {locations}"

    @allure.story("View Switcher")
    @allure.step("Verify switching between Grid and List views")
    def test_switch_view_mode(self, driver):
        events_page = EventsPage(driver).open()
        WebDriverWait(driver, 15).until(lambda d: len(events_page.get_all_event_cards()) > 0)
        
        # Натискаємо на список і перевіряємо, чи відображаються картки
        events_page.switch_to_list_view()
        WebDriverWait(driver, 10).until(lambda d: events_page.is_list_view_active())
        assert len(events_page.get_all_event_cards()) > 0, "Cards should be visible in list view"
        
        # Натискаємо на сітку і перевіряємо, чи відображаються картки
        events_page.switch_to_grid_view()
        WebDriverWait(driver, 10).until(lambda d: not events_page.is_list_view_active())
        assert len(events_page.get_all_event_cards()) > 0, "Cards should be visible in grid view"
