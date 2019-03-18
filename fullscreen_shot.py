# coding=utf-8

import os
import time
from selenium import webdriver
from PIL import Image

driver = webdriver.Chrome()
driver.get('https://phptravels.com/demo/')
driver.maximize_window()


def fullpage_screenshot(driver, file):
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    rectangles = []
    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height
        if top_height > total_height:
            top_height = total_height
        while ii < total_width:
            top_width = ii + viewport_width
            if top_width > total_width:
                top_width = total_width
            rectangles.append((ii, i, top_width, top_height))
            ii = ii + viewport_width
        i = i + viewport_height
    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0
    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)
        file_name = "part_{0}.png".format(part)
        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)
        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])
        stitched_image.paste(screenshot, offset)
        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle
    stitched_image.save(file)
    return True


fullpage_screenshot(driver, 'phptravels_demo.png')
driver.get('https://www.phptravels.net/public/expedia/')
driver.maximize_window()
fullpage_screenshot(driver, 'phptravels_expedia.png')
driver.get('https://www.phptravels.net/public/expedia/offers')
driver.maximize_window()
fullpage_screenshot(driver, 'phptravels_expedia_offers.png')

driver.quit()
# kill all chromedriver instances
os.system('taskkill /F /IM chromedriver.exe')
