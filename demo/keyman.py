import config
import time
from selenium.webdriver.common.by import By
from util import click_element, hide_overlay, create_fullpage_overlay, create_overlay, show_page


class Keyman:
    def _type(self, element, keys):
        for char in keys:
            element.send_keys(char)
            time.sleep(0.5)

    def _search_keyman_com(self):
        config.driver.get('https://keyman.com/')
        config.driver.find_element(By.XPATH, '//div[@id="keyboards"]').click()
        config.driver.find_element(By.ID, 'language-search').send_keys('amharic')
        config.driver.find_element(By.ID, 'search-submit').click()
        time.sleep(2)
        config.driver.find_element(By.XPATH, '//a[text()="GFF Amharic"]').click()
        time.sleep(2)
        config.driver.find_element(By.XPATH, '//div[@id="try-keymanweb-link"]/div/a').click()
        time.sleep(2)
        textarea = config.driver.find_element(By.ID, 'message')
        textarea.click()
        self._type(textarea, 'Tiena ysTIN')
        time.sleep(2)

    def presentation_p1(self, url):
        config.driver.get(url)
        time.sleep(5)
        config.driver.execute_script("""
            document.getElementById('first').classList.add('animate-out');
            const second = document.getElementById('second')
            second.classList.remove('hidden');
            second.classList.add('animate-in');
            """)
        time.sleep(20)
        config.driver.execute_script("""
            document.getElementById('second').classList.add('animate-out');
            """)

    def rundemo(self, url):
        self.presentation_p1(url)
        self._search_keyman_com()
