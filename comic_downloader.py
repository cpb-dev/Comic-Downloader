import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_auto_update import check_driver
import urllib.request as req
import urllib.error
from os import listdir
import os
from glob import glob
import img2pdf
import shutil

check_driver('/Users/cpbai/AppData/Local/Programs/Python/Python310/Lib/site-packages/selenium/webdriver')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(
    service= Service('/Users/cpbai/AppData/Local/Programs/Python/Python310/Lib/site-packages/selenium/webdriver/chromedriver.exe'),
    options = options,
)

def gather_comic():
    url = "https://readallcomics.com/nightwing-v4-101-2023/"
    x_path = "/html/body/div[2]/p/img"

    browser.get(url)

    img_dir = "C:/Users/cpbai/PlayGrounds/Comic Downloader/tmp/"
    images = []

    for img in browser.find_elements(by = "xpath", value = x_path):
        image = img.get_attribute('src')
        images.append(image)
    
    for i in range(len(images)):
        #Create a temporary file for image before pdf
        file = img_dir + "Nightwing00{}.jpg".format(i)
        with req.urlopen(images[i]) as d, open(file, "wb") as opfile:
            data = d.read()
            opfile.write(data)

    pdf_path = "C:/Users/cpbai/PlayGrounds/Comic Downloader/Comics/new_comic.pdf"

    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(sorted(glob(os.path.join(img_dir, "*.jpg")), key=len)))

    for filename in os.listdir(img_dir):
        filepath = os.path.join(img_dir, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)

gather_comic()

#Control the page to go to next comic, if comic already exists
#Better organise how the comics are saved and ordered