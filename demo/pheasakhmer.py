import config
import time
from util import click_element, hide_overlay, create_fullpage_overlay, create_overlay, show_page_typewriter, wait

class PheasaKhmer:
    def select_and_run_example(self, example, text):
        click_element("//div[@id='dropdown-examples']/ul/li/button[@data-examples='#example0']")
        click_element(f"//div[@id='{example}']//button")
        config.driver.execute_script(f"""
            const textarea = document.getElementById('ta1');
            const overlay = document.getElementById('demo-overlay');
            const text = document.getElementById('demo-text');
            // hide overlay
            textarea.onfocus = function() {{ text.innerText = 'got focus'; overlay.style['display'] = 'none'; }};
            text.innerText = '{text}';
            overlay.style['display'] = 'block';
            """)
        wait(5)
        hide_overlay()


    def rundemo(self, url):
        config.driver.get(url)
        create_fullpage_overlay()
        create_overlay()
        wait(1)
        click_element("//label[@for='btn-language-english']", False)
        wait(1)
        click_element("//button[@id='help-ok']", False)
        wait(1)
        show_page_typewriter('Das Alphabet von Khmer hat 74 Buchstaben. Manche Vokale werden vor den Konsonanten geschrieben, aber danach gesprochen. Die Frage ist nun, wie schreibt man das am Computer: so wie es da steht (erst Vokal, dann Konsonant) oder so wie es gesprochen wird (erst Konsonant, dann Vokal)?', False)
        show_page_typewriter('Bei der Anzeige macht es keinen Unterschied, aber es wird unterschiedlich gespeichert, und deshalb zeigen z.B. Suchen unterschiedliche Ergebnisse.', False)
        show_page_typewriter('Das Wort ខ្មែរ („Khmer“) kann auf zwei Arten geschrieben werden:', True)
        wait(1)
        click_element("//button[@id='btn-examples']")
        self.select_and_run_example('example-1', 'richtige Reihenfolge')
        wait(5)
        self.select_and_run_example('example-2', 'falsche Reihenfolge')
        wait(5)
