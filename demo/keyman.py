import config
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from util import click_element, hide_overlay, create_fullpage_overlay, create_overlay, show_page, wait


class Keyman:
    def _type(self, element, keys):
        # TODO: highlight typed key
        for char in keys:
            element.send_keys(char)
            time.sleep(0.5)

    def _load_page(self, url):
        config.driver.get(url)

    def _presentation_p1(self, url):
        self._load_page(url)
        wait(5)
        config.driver.execute_script("""
            document.getElementById('first').classList.add('animate-out');
            const second = document.getElementById('second')
            second.classList.remove('hidden');
            second.classList.add('animate-in');
            """)
        wait(15)
        config.driver.execute_script("""
            document.getElementById('second').classList.add('animate-out');
            """)

    def _get_textarea_and_type(self, keys):
        textarea = config.driver.find_element(By.ID, 'message')
        textarea.click()
        self._type(textarea, keys)
        return textarea

    def _enable_keyboard(self, keyboard):
        config.driver.find_element(By.XPATH, f'//a[@title="Select {keyboard} keyboard"]').click()

    def _disable_keyboard(self):
        config.driver.find_element(By.XPATH, f'//a[@title="Turn off KeymanWeb keyboards"]').click()

    def _increase_font_size(self):
        slider = config.driver.find_element(By.ID, 'slider')
        actions = ActionChains(config.driver)
        actions.move_to_element(slider).click_and_hold().move_by_offset(0, 250).release().perform()
        config.driver.execute_script("""
            const btn = document.getElementById('kmw_btn_osk');
            if (btn.classList.contains('kmw_btn_disabled')) {{
                btn.classList.remove('kmw_btn_disabled');
            }}
            btn.click();
            """)

    def _search_keyman_com(self):
        self._load_page('https://keyman.com/')
        create_fullpage_overlay()
        config.driver.find_element(By.XPATH, '//div[@id="keyboards"]').click()
        config.driver.find_element(By.ID, 'language-search').send_keys('amharic')
        config.driver.find_element(By.ID, 'search-submit').click()
        wait(2)
        config.driver.find_element(By.XPATH, '//a[text()="GFF Ethiopic"]').click()
        wait(2)
        config.driver.find_element(By.XPATH, '//div[@id="try-keymanweb-link"]/div/a').click()
        wait(2)
        self._increase_font_size()
        self._enable_keyboard('GFF Ethiopic')
        self._get_textarea_and_type('Tiena ysTlN')
        wait(2)
        self._disable_keyboard()

    def _keyman_rules(self):
        show_page('Regeln erlauben es, Zeichen je nach Kontext und gedrückter Taste zu ändern.', True, 10)
        self._enable_keyboard('GFF Ethiopic')
        textarea = self._get_textarea_and_type('\n')
        wait(1)
        self._type(textarea, 'S')
        wait(1)
        self._type(textarea, 'S')
        wait(1)
        self._type(textarea, 'S')
        wait(1)
        self._disable_keyboard()
        show_page('Keyman ist besonders für komplexe Schreibsysteme hilfreich, wie z.B. für Khmer, eine Sprache, die in Kambodscha gesprochen und geschrieben wird.', True, 10)
        self._load_page('https://keymanweb.com/#km,Keyboard_khmer_angkor')
        self._increase_font_size()
        self._enable_keyboard('Khmer Angkor')
        textarea = self._get_textarea_and_type('xjmEr')
        wait(2)
        self._disable_keyboard()

    def rundemo(self, url):
        self._presentation_p1(url)
        self._search_keyman_com()
        self._keyman_rules()
