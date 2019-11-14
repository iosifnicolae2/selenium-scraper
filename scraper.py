import os
import platform
import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TIMEOUT = 5 # seconds

WEBDRIVER_EXECUTABLE_PATH = None
operating_system = platform.system()

if operating_system == 'Darwin':
    WEBDRIVER_EXECUTABLE_PATH = 'webdrivers/geckodriver_macos'

if operating_system == 'Windows':
    WEBDRIVER_EXECUTABLE_PATH = 'webdrivers/geckodriver_windows_32.exe'

if not WEBDRIVER_EXECUTABLE_PATH:
    raise Exception("Your operating system is not supported!")


def task1():
    browser = Firefox(executable_path='webdrivers/geckodriver_macos')
    browser.get('http://example.com/')
    # Wait 1s
    time.sleep(1)
    browser.save_screenshot(os.path.abspath('screeenshots/example__initial_page.png'))

    # Click on "More information" button
    more_information_button = browser.find_element_by_css_selector("body > div > p:nth-child(3) > a")
    more_information_button.click()
    browser.save_screenshot(os.path.abspath('screeenshots/example__more_information_page.png'))
    browser.quit()

def task2():
    browser = Firefox(executable_path='webdrivers/geckodriver_macos')
    browser.get('http://bandcamp.com/')
    browser.save_screenshot(os.path.abspath('screeenshots/bandcamp__initial_page.png'))

    # Click on "More information" button
    searchbox = browser.find_element_by_css_selector("#autocomplete-form > input.you-autocomplete-me.dismiss-tooltip-alt")
    searchbox.send_keys("Lady Gaga")
    searchbox.send_keys(Keys.ENTER)
    browser.save_screenshot(os.path.abspath('screeenshots/bandcamp__after_search.png'))

    WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'album')))

    all_albumns = browser.find_elements_by_css_selector(".album")
    album_names = []
    for album in all_albumns:
        album_id = album.find_element_by_css_selector(".heading").text
        album_names.append(album_id)

    print("Albums:\n {}".format('\n '.join(album_names)))

    listened_songs = []
    LISTEN_X_ALBUMS = 5
    for album_id in range(LISTEN_X_ALBUMS):
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'album')))
        all_albumns = browser.find_elements_by_css_selector(".album")
        album_title = all_albumns[album_id].find_element_by_css_selector(".heading")
        first_album_link = album_title.find_element_by_css_selector("a")

        listened_songs.append((album_title.text, first_album_link.get_attribute("href")))

        first_album_link.click()
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'playbutton')))
        play_btn = browser.find_element_by_css_selector('.playbutton')
        play_btn.click()
        browser.save_screenshot(os.path.abspath('screeenshots/bandcamp__album_page_{}.png'.format(album_id)))
        # Listen 5s
        time.sleep(5)
        # Go back
        browser.execute_script("window.history.go(-1)")

    listened_songs_txt = "Listened songs:\n{}".format('\n'.join([" - " + song + ": " + url for song, url in listened_songs]))
    print(listened_songs_txt)
    with open("listened_songs.txt", "w") as text_file:
        text_file.write(listened_songs_txt)

    browser.quit()


if __name__ == '__main__':
    task1()
    task2()
