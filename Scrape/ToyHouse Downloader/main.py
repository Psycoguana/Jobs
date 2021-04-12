import os
import re
import pathlib
import time
from typing import List
from configparser import ConfigParser

import requests

from bs4 import BeautifulSoup, Tag

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class Bot:
    def __init__(self):
        self.url = "https://toyhou.se/"

        config = ConfigParser()
        config.read('config.ini')
        self.folder = config['DEFAULT']['FOLDER']
        self.username = config['DEFAULT']['USERNAME']
        self.password = config['DEFAULT']['PASSWORD']
        self.wanted_user = config['DEFAULT']['PROFILE']

        self.session = requests.Session()

    def main(self):
        print("\n\rLogging in...", end='', flush=True)
        self.login()
        print("Login completed!\n")

        characters: List[Tag] = self.get_raw_characters()

        print("Creating folders...")
        self.create_folders([x.text for x in characters])

        self.download_characters([x['href'] for x in characters])

    def login(self):
        # Silence WebDriver Manager.
        os.environ['WDM_LOG_LEVEL'] = '0'

        options = Options()
        options.headless = True
        # Turn off debugging in Windows.
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(self.url)

        # Wait until the page loads the login button.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-target="#modal-login"]'))
        )
        element.click()

        # Wait until the login form appears and is clickable.
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login_username'))
        )

        username_input = driver.find_element_by_id('login_username')
        username_input.click()
        username_input.send_keys(self.username)

        password_input = driver.find_element_by_id('login_password')
        password_input.click()
        password_input.send_keys(self.password)

        submit_form = driver.find_element_by_css_selector('input[type="submit"]')
        submit_form.click()

        # Wait until the login alert is showing, so we're sure we logged in successfully.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        # Pass the selenium cookies to requests, so we can continue with requests.Session which is WAY faster.
        cookies = driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        # Close the browser.
        driver.close()

    def get_raw_characters(self) -> List[Tag]:
        raw_website = self.session.get(self.url + self.wanted_user + '/characters').content
        website = BeautifulSoup(raw_website, 'html.parser')

        characters_table = website.select('span.thumb-character-name > a')
        return characters_table

    def create_folders(self, folders: List[str]):
        for folder in folders:
            pathlib.Path(self.folder + '/' + folder).mkdir(parents=True, exist_ok=True)

    def download_characters(self, characters):
        for character in characters:
            raw_gallery = self.session.get(self.url + character[1:] + '/gallery').content
            gallery = BeautifulSoup(raw_gallery, 'html.parser')
            name = gallery.select_one('h1.image-gallery-title > a').text
            characters = gallery.select('a.magnific-item')

            print(f"\nDownloading: {name}")
            characters = [x['href'] for x in characters]
            self.download_gallery(name, characters)

    def download_gallery(self, character, links):
        for i, link in enumerate(links, start=1):
            print(f"\r\tDownloading image {i}/{len(links)}", end='', flush=True)
            # Here i take only the image name, to use it as a filename when downloading the image.
            pattern = r"(.+images\/)(.+\.[jpg|jpeg|png|gif]{3,4})"
            match = re.search(pattern, link)
            base_image_link = match.group(1)
            link = match.group(2)

            file_path = os.path.join(self.folder, character, link)
            # Download the file if it hasn't been downloaded before.
            if not os.path.exists(file_path):
                self.download_image(file_path, image_link=base_image_link + link)

    def download_image(self, file_path, image_link):
        with open(file_path, 'wb') as file:
            content = self.session.get(image_link).content
            file.write(content)


if __name__ == '__main__':
    t0 = time.time()
    bot = Bot()
    bot.main()
    print(f"\n\nExec time: {(time.time() - t0):.2f} seconds.")
