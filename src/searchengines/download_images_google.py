# Resources:
# https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import sys
import os
from pathlib import Path
import urllib3
import argparse
import urllib.request

searchterm = 'banderas' # will also be the name of the folder
url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getImagesFromGoogle(searchterm, dstDir, chromedriverdir):
    browser = webdriver.Chrome(chromedriverdir + '/chromedriver', options=chrome_options)
    browser.get(url)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    counter = 0
    succounter = 0

    print("start scrolling to generate more images on the page...")
    # 500 time we scroll down by 10000 in order to generate more images on the website
    #for _ in range(10):
     #   browser.execute_script("window.scrollBy(0,10000)")

    Path(dstDir).mkdir(parents=True, exist_ok=True)

    print("start scraping ...")
    #for x in browser.find_elements_by_xpath('//img[contains(@class,"rg_i Q4LuWd tx8vtf")]'):
    for x in browser.find_elements_by_xpath('//img[contains(@class,"rg_i Q4LuWd")]'):
        counter = counter + 1
        print("Total Count:", counter)
        print("Succsessful Count:", succounter)
        print("URL:", x.get_attribute('src'))

        img = x.get_attribute('src')
        new_filename = "image"+str(counter)+".jpg"

        try:
            file_path = dstDir
            file_path += new_filename
            urllib.request.urlretrieve(img, file_path)
            succounter += 1
        except Exception as e:
            print(e)

    print(succounter, "pictures succesfully downloaded")
    browser.close()

#getImagesFromGoogle(searchterm)