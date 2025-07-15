#!/usr/bin/env python3

import time
from selenium import webdriver
#from webdriver_manager.firefox import GeckoDriverManager

def click_element(xpath):
    driver.find_element("xpath", xpath).click()
    time.sleep(1)


def create_fullpage_overlay():
    # https://www.w3schools.com/howto/howto_css_overlay.asp
    driver.execute_script("""
        const overlay = document.createElement("div");
        overlay.id = 'demo-fullpage-overlay';
        overlay.style['position'] = 'fixed';
        overlay.style['display'] = 'none';
        overlay.style['width'] = '100%';
        overlay.style['height'] = '100%';
        overlay.style['top'] = 0;
        overlay.style['left'] = 0;
        overlay.style['right'] = 0;
        overlay.style['bottom'] = 0;
        overlay.style['background-color'] = 'rgba(255,255,255,0.8)';
        overlay.style['z-index'] = 2;
        overlay.style['cursor'] = 'pointer';
        const text = document.createElement("div");
        text.id = "demo-fullpage-text";
        text.style['position'] = 'absolute';
        text.style['top'] = '50%';
        text.style['left'] = '50%';
        text.style['font-size'] = '40px';
        text.style['color'] = 'black';
        text.style['transform'] = 'translate(-50%,-50%)';
        text.style['-ms-transform'] = 'translate(-50%,-50%)';
        text.style['font-family'] = 'Times';
        overlay.appendChild(text);
        document.body.appendChild(overlay);
        """)


def create_overlay():
    # https://www.w3schools.com/howto/howto_css_overlay.asp
    driver.execute_script("""
        const overlay = document.createElement("div");
        overlay.id = 'demo-overlay';
        overlay.style['position'] = 'fixed';
        overlay.style['display'] = 'none';
        overlay.style['width'] = '100%';
        overlay.style['height'] = '100%';
        overlay.style['top'] = 0;
        overlay.style['left'] = 0;
        overlay.style['right'] = 0;
        overlay.style['bottom'] = 0;
        // overlay.style['background-color'] = 'rgba(0,0,0,0.5)';
        overlay.style['z-index'] = 2;
        overlay.style['cursor'] = 'pointer';
        const text = document.createElement("div");
        text.id = "demo-text";
        text.style['position'] = 'absolute';
        text.style['top'] = '80%';
        text.style['left'] = '50%';
        text.style['font-size'] = '80px';
        text.style['color'] = 'red';
        text.style['transform'] = 'translate(-50%,-50%)';
        text.style['-ms-transform'] = 'translate(-50%,-50%)';
        overlay.appendChild(text);
        document.body.appendChild(overlay);
        """)


def set_overlay_text(text):
    driver.execute_script(f"""
        document.getElementById('demo-text').innerText = '{text}';
        document.getElementById('demo-overlay').style['display'] = 'block';
        """)


def hide_overlay():
    driver.execute_script("document.getElementById('demo-overlay').style['display'] = 'none';")


def select_and_run_example(example, text):
    click_element("//div[@id='dropdown-examples']/ul/li/button[@data-examples='#example0']")
    click_element(f"//div[@id='{example}']//button")
    driver.execute_script(f"""
        const textarea = document.getElementById('ta1');
        const overlay = document.getElementById('demo-overlay');
        const text = document.getElementById('demo-text');
        textarea.onfocus = function() {{ text.innerText = 'got focus'; overlay.style['display'] = 'none'; }};
        text.innerText = '{text}';
        overlay.style['display'] = 'block';
        """)
    time.sleep(5)
    hide_overlay()


def show_overlay(text, length):
    set_overlay_text(text)
    time.sleep(length)
    hide_overlay()


def show_page(text, hide):
    speed = 100
    waittime = len(text) * speed / 1000 + 2
    print(f'waitime={waittime} for {text}')
    driver.execute_script(f"""
        document.getElementById('demo-fullpage-overlay').style['display'] = 'block';
        const textDiv = document.getElementById('demo-fullpage-text');
        textDiv.innerHTML = '';
        var i = 0;
        const speed = {speed};
        const text = '{text}';

        function typeWriter() {{
            if (i < text.length) {{
                console.log('i=' + i + ', text[i]=' + text.charAt(i));
                textDiv.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }}
        }}

        typeWriter();
        """)
    time.sleep(waittime)
    if hide:
        driver.execute_script("document.getElementById('demo-fullpage-overlay').style['display'] = 'none';")


def main():
    driver.get("https://ភាសាខ្មែរ.com/")
    create_fullpage_overlay()
    create_overlay()
    click_element("//label[@for='btn-language-english']")
    click_element("//button[@id='help-ok']")
    show_page('In Khmer (Sprache die in Kambodscha gesprochen wird) werden manche Vokale vor den Konsonanten geschrieben, aber danach gesprochen. Die Frage ist nun, wie schreibt man das am Computer: so wie es da steht (erst Vokal, dann Konsonant) oder so wie es gesprochen wird?', False)
    show_page('Von der Darstellung macht es keinen Unterschied, aber es wird unterschiedlich gespeichert, und deshalb zeigen z.B. Suchen unterschiedliche Ergebnisse.', False)
    show_page('Die folgende Demo zeigt einige Beispiele', True)
    time.sleep(1)
    click_element("//button[@id='btn-examples']")
    select_and_run_example('example-1', 'Hello world!')
    time.sleep(5)
    driver.quit()


driver = webdriver.Firefox()
main()
