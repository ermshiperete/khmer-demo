import config
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from util import click_element, hide_overlay, show_overlay, show_page, wait


class Keyman:
    def __press_key(self, key, isShift, press):
        layer = 'shift' if isShift else 'default'
        vkey = f'{layer}-K_{key.upper()}'

        config.driver.execute_script("""
            const vkey = arguments[0];
            const pressed = arguments[1];
            const isShift = arguments[2];

            if (pressed && isShift) {
                keyman.osk.vkbd.layerId = 'shift';
            }
            const element = document.getElementById(vkey);
            if (!element) {
                alert(`Key ${vkey} not found`);
                return;
            }

            const x = keyman.util.getAbsoluteX(element);
            const y = keyman.util.getAbsoluteY(element);
            if (pressed) {
                element.style.background = 'green';
                element.dispatchEvent(new MouseEvent('mousedown', {clientX: x, clientY: y, buttons: 1}));
                element.dispatchEvent(new MouseEvent('mouseup', {clientX: x, clientY: y, buttons: 1}));
            } else {
                element.style.background = '';
                element.dispatchEvent(new MouseEvent('mouseup', {clientX: x, clientY: y, buttons: 1}));
                if (isShift) {
                    keyman.osk.vkbd.layerId='default';
                }
            }
            """, vkey, press, isShift)

    def __show_pressed_key(self, char, pressed):
        if char.isupper():
            self.__press_key(char, True, pressed)
        elif char.isspace():
            self.__press_key('space', False, pressed)
        elif char == '\n':
            self.__press_key('enter', False, pressed)
        elif char == '\t':
            self.__press_key('tab', False, pressed)
        else:
            self.__press_key(char, False, pressed)

    def _type(self, keys):
        for char in keys:
            self.__show_pressed_key(char, True)
            time.sleep(2)
            self.__show_pressed_key(char, False)

    def _load_page(self, url):
        config.driver.get(url)

    def _next_page(self, new, waittime):
        config.driver.execute_script(f"""
            const newPage = 'pg{new}';
            const oldElems = document.querySelector(".current");
            if (oldElems) {{
                oldElems.classList.remove('current');
                oldElems.classList.add('animate-out');
                oldElems.classList.add('hidden');
            }}
            const newElem = document.getElementById(newPage);
            newElem.classList.remove('hidden');
            newElem.classList.add('curent');
            newElem.classList.add('animate-in');
            """)
        wait(waittime)
        config.driver.execute_script(f"""
            const newElem = document.getElementById('pg{new}');
            newElem.classList.add('animate-out');
            """)

    def _show_presentation_page(self, url):
        self._load_page(url)
        wait(2)
        self._next_page(1, 5)
        self._next_page(2, 13)
        self._next_page(3, 13)
        self._next_page(4, 13)
        self._next_page(5, 23)
        self._next_page(6, 23)
        config.driver.execute_script(f"""
            const oldElems = document.getElementsByClassName('current');
            if (oldElems && oldElems.length > 0) {{
                oldElems.classList.remove('current');
                oldElems.classList.add('hidden');
            }}
            """)

    def continue_presentation(self, url):
        self._load_page(url)
        self._next_page(7, 18)
        self._next_page(8, 18)
        self._next_page(9, 15)
        self._next_page(10, 15)
        self._next_page(11, 10)
        self._next_page(12, 15)
        self._next_page(13, 15)

    def _get_textarea_and_type(self, keys):
        textarea = config.driver.find_element(By.ID, 'message')
        textarea.click()
        config.driver.execute_script("document.getElementById('message').value = ''")
        self._type(keys)
        return textarea

    def _enable_keyboard(self, keyboard):
        config.driver.find_element(By.XPATH, f'//a[@title="Select {keyboard} keyboard"]').click()

    def _disable_keyboard(self):
        config.driver.find_element(By.XPATH, '//a[@title="Turn off KeymanWeb keyboards"]').click()

    def _increase_font_size(self):
        slider = config.driver.find_element(By.ID, 'slider')
        actions = ActionChains(config.driver)
        actions.move_to_element(slider).click_and_hold().move_by_offset(0, 300).release().perform()
        config.driver.execute_script("""
            const btn = document.getElementById('kmw_btn_osk');
            if (btn.classList.contains('kmw_btn_disabled')) {
                btn.classList.remove('kmw_btn_disabled');
            }
            btn.click();
            """)

    def _search_keyman_com(self):
        self._load_page('https://keyman.com/')
        show_overlay('Suche nach einer Tastatur für Amharisch', 0, False, transparent=True)
        config.driver.find_element(By.XPATH, '//div[@id="keyboards"]').click()
        config.driver.find_element(By.ID, 'language-search').send_keys('amharic')
        config.driver.find_element(By.ID, 'search-submit').click()
        show_overlay('Suche nach einer Tastatur für Amharisch', 0, False, transparent=True)
        wait(5)
        gff_ethiopic = config.driver.find_element(By.XPATH, '//a[text()="GFF Ethiopic"]')
        config.driver.execute_script("arguments[0].parentElement.parentElement.previousSibling.scrollIntoView();", gff_ethiopic)
        gff_ethiopic.click()
        show_overlay('Suche nach einer Tastatur für Amharisch', 0, False, transparent=True)
        wait(5)
        button = config.driver.find_element(By.XPATH, '//div[@id="try-keymanweb-link"]/div/a')
        config.driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        show_overlay('Amharische Tastatur', 0, False, transparent=True)
        wait(5)
        footerRect = config.driver.find_element(By.CLASS_NAME, 'footer').rect
        show_overlay('„Hallo“ (ጤና ይስጥልኝ) auf Amharisch', 5, False, top=footerRect['y'] + footerRect['height'])
        self._increase_font_size()
        self._enable_keyboard('GFF Ethiopic')
        self._get_textarea_and_type('Tiena ysTlN')
        wait(5)
        self._disable_keyboard()
        hide_overlay()
        return

    def _keyman_rules(self):
        show_page('Für jede Sprache werden in Keyman Regeln hinterlegt. Diese Regeln erlauben es, Zeichen je nach Kontext und gedrückter Taste zu ändern. Die Regeln sind im Hintergrund in der Tastatur aktiv.', True, 10)
        footerRect = config.driver.find_element(By.CLASS_NAME, 'footer').rect
        show_overlay('Zum Beispiel: Mehrfaches Drücken von Shift+S erzeugt verschiedene Zeichen.', 5, False, top=footerRect['y'] + footerRect['height'])
        self._enable_keyboard('GFF Ethiopic')
        self._get_textarea_and_type('S')
        wait(1)
        self._type('S')
        wait(1)
        self._type('S')
        wait(1)
        self._disable_keyboard()
        hide_overlay()
        self._load_page('https://keymanweb.com/#km,Keyboard_khmer_angkor')
        config.driver.refresh()
        wait(3)
        self._disable_keyboard()
        show_page('Keyman ist besonders für komplexe Schreibsysteme ein geniales Werkzeug. Ein Beispiel dafür ist Khmer, eine Sprache, die in Kambodscha gesprochen und geschrieben wird.', True, 8)
        show_overlay('ខ្មែរ („Khmer“) in Khmer geschrieben', 5, False)
        self._increase_font_size()
        self._enable_keyboard('Khmer Angkor')
        self._get_textarea_and_type('xjmEr')
        wait(5)
        self._disable_keyboard()
        hide_overlay()

    def rundemo(self, url):
        self._show_presentation_page(url)
        self._search_keyman_com()
        self._keyman_rules()
