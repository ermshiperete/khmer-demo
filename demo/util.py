#!/usr/bin/env python3
import time
import config
from selenium.webdriver.common.by import By


def click_element(xpath, wait=True):
    config.driver.find_element("xpath", xpath).click()
    if wait:
        time.sleep(1)


def create_fullpage_overlay():
    # https://www.w3schools.com/howto/howto_css_overlay.asp
    config.driver.execute_script("""
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


def _create_overlay(top='80%'):
    # https://www.w3schools.com/howto/howto_css_overlay.asp
    config.driver.execute_script(f"""
        const overlay = document.createElement("div");
        overlay.id = 'demo-overlay';
        overlay.style['position'] = 'fixed';
        overlay.style['display'] = 'none';
        overlay.style['width'] = '100%';
        overlay.style['height'] = '20%';
        overlay.style['top'] = '{top}';
        overlay.style['left'] = 0;
        overlay.style['right'] = 0;
        overlay.style['bottom'] = 0;
        // overlay.style['background-color'] = 'rgba(0,0,0,0.5)';
        overlay.style['z-index'] = 2;
        overlay.style['cursor'] = 'pointer';
        const text = document.createElement("div");
        text.id = "demo-text";
        text.style['position'] = 'absolute';
        text.style['top'] = 0;
        text.style['left'] = '10%';
        text.style['font-size'] = '40px';
        text.style['color'] = 'red';
        text.style['text-align'] = 'center';
        text.style['margin'] = 0;
        // text.style['transform'] = 'translate(-50%,-50%)';
        // text.style['-ms-transform'] = 'translate(-50%,-50%)';
        overlay.appendChild(text);
        document.body.appendChild(overlay);
        """)


def _set_overlay_text(text, top):
    if len(config.driver.find_elements(By.ID, 'demo-overlay')) <= 0:
        _create_overlay(top)

    config.driver.execute_script(f"""
        document.getElementById('demo-text').innerText = '{text}';
        document.getElementById('demo-overlay').style['display'] = 'block';
        """)


def hide_overlay():
    config.driver.execute_script("document.getElementById('demo-overlay').style['display'] = 'none';")


def show_overlay(text, duration, hide=True, top=None):
    _set_overlay_text(text, top)
    if hide:
        wait(duration)
        hide_overlay()


def show_page_typewriter(text, hide):
    if len(config.driver.find_elements(By.ID, 'demo-fullpage-overlay')) <= 0:
        create_fullpage_overlay()

    speed = 100
    waittime = len(text) * speed / 1000 + 2
    config.driver.execute_script(f"""
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
    wait(waittime)
    if hide:
        config.driver.execute_script("document.getElementById('demo-fullpage-overlay').style['display'] = 'none';")


def show_page(text, hide, waittime):
    if len(config.driver.find_elements(By.ID, 'demo-fullpage-overlay')) <= 0:
        create_fullpage_overlay()

    config.driver.execute_script(f"""
        document.getElementById('demo-fullpage-overlay').style['display'] = 'block';
        const textDiv = document.getElementById('demo-fullpage-text');
        textDiv.innerHTML = '{text}';
        """)
    wait(waittime)
    if hide:
        config.driver.execute_script("document.getElementById('demo-fullpage-overlay').style['display'] = 'none';")


def _create_progress_bar():
    config.driver.execute_script("""
        const bottom = document.createElement("div");
        bottom.id = 'bottom';
        bottom.style['width'] = '100%';
        bottom.style['position'] = 'absolute';
        bottom.style['bottom'] = 0;
        const pbar = document.createElement("progress");
        pbar.id = 'pbar';
        pbar.style['width'] = '100%';
        pbar.style['height'] = '5px';
        pbar.style['position'] = 'relative';
        pbar.style['bottom'] = 0;
        pbar.style['background-color'] = 'white';
        pbar.style['border'] = 'none';
        pbar.style['color'] = 'blue';
        bottom.appendChild(pbar);
        document.body.appendChild(bottom);
        """)


def wait(seconds):
    if len(config.driver.find_elements(By.ID, 'pbar')) <= 0:
        _create_progress_bar()

    config.driver.execute_script(f"""
        const pbar = document.getElementById('pbar');
        pbar.value = {seconds*10};
        pbar.max = {seconds*10};
        function start_countdown() {{
            var reverse_counter = {seconds*10};
            var downloadTimer = setInterval(function(){{
                document.getElementById("pbar").value = --reverse_counter;
                if(reverse_counter <= 0)
                    clearInterval(downloadTimer);
            }},100);
        }}

        start_countdown();
        """)
    time.sleep(seconds)

