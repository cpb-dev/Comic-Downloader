import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_auto_update import check_driver
import urllib.request as req
import urllib.error
from os import listdir
import os, time
from glob import glob
import img2pdf
import shutil
import pandas as pd

this_file = os.path.dirname(__file__)

check_driver('/Users/cpbai/AppData/Local/Programs/Python/Python310/Lib/site-packages/selenium/webdriver')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
browser = webdriver.Chrome(
    service= Service('/Users/cpbai/AppData/Local/Programs/Python/Python310/Lib/site-packages/selenium/webdriver/chromedriver.exe'),
    options = options,
)

def printProgress(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = '\r'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print("\n")


def gatherComic(url, comic, issue):
    x_path = "/html/body/div[2]/p/img"

    browser.get(url)

    img_dir = os.path.join(this_file, "temp")
    images = []

    for img in browser.find_elements(by = "xpath", value = x_path):
        image = img.get_attribute('src')
        images.append(image)
    
    length = len(images) #length of whater the progress bar is for
    printProgress(0, length, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for i in range(len(images)):
        #Create a temporary file for image before pdf
        file = os.path.join(img_dir, comic + "{}.jpg".format(i))
        with req.urlopen(images[i]) as d, open(file, "wb") as opfile:
            data = d.read()
            opfile.write(data)

        printProgress(i + 1, length, prefix = 'Progress:', suffix = 'Complete', length = 50)

    pdf_path = os.path.join(this_file, "Comics", comic + " " + issue + ".pdf")

    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(sorted(glob(os.path.join(img_dir, "*.jpg")), key=len)))

    for filename in os.listdir(img_dir):
        filepath = os.path.join(img_dir, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)

    print("Download Complete!")
    time.sleep(2)

def getComicSeries(hero):
    data = pd.read_csv(os.path.join(this_file, "comics.csv"))
    temp_data = data[data['Hero'] == hero]
    hero = temp_data.at[0, 'Hero']
    title = temp_data.at[0, 'Series Title']
    issue = str(temp_data.at[0,'Current Issue'])
    year = temp_data.at[0,'Year']
    url = temp_data.at[0, "URL"]
    browser.get(url)

    x_path = "//li/a[@title='{} {} ({})']".format(title, issue.zfill(3), year)
    new_url = browser.find_element(by = "xpath", value = x_path).get_attribute("href")

    #TODO: Need to amend original csv to update current issue
    #TODO: Could implement a way to iterate through all issues to the most up-to-date
    
    gatherComic(new_url, hero, issue)
    
if __name__ == "__main__":
    hero =  input("What hero are you downloading a comic for?\n")
    issue = input("Issue No. ")
    url = input("Input URL: ")

    gatherComic(url, hero, issue)
    #num = "005"

    #num2 = int(num) + 2
    #print(str(num2).zfill(3))
    #getComicSeries("Nightwing")
