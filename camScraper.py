#Must Haves
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import urllib

import time
from bs4 import BeautifulSoup
import datetime

#Data Processing and Stats!
import pandas as pd
import numpy as np

#Regex
import re

#For Image Plots
import matplotlib.image as im
import matplotlib.pyplot as plt

#File Org
import glob
import os
import sys

def clean_img_address(a):
    a = a.replace(" ","_")
    a = a.replace("@","at")
    a = a.replace("/","_")
    a = a.replace(".","")
    return a

def find_element(containing_el, search_term, attribute):
    n_el = 0
    needle = None
    for el in containing_el.find_elements(By.XPATH, ".//*"):
        n_el += 1
        att_value = el.get_attribute(attribute)
        if att_value:
            if search_term in att_value:
                needle = el
                return needle
def get_address_borough(trow):
    cb_cell, a_cell, b_cell =  trow.find_elements(By.TAG_NAME, 'td')[:3]
    return (cb_cell, a_cell.text, b_cell.text)

def parse_row_text(row_text):
    boroughs = ['Manhattan','Bronx','Staten Island','Queens','Brooklyn']
    borough = [b for b in boroughs if b in row_text][0]
    address = row_text.replace(borough,"")
    return address, borough

sys.path.append('/home/matt/Documents/Projects/rpa_recording/chromedriver-linux64/chromedriver')


class camScraper:
    def __init__(self, iterations=10**3, last_row_scraped=0, headless=False):
        if sys.platform == 'linux':
            pass
        else:
            self.geckoDriverPath = '/Users/matthewmitchell/Documents/Projects/Tools/Python/Scraping/geckodriver'
        self.camera_tables = []
        self.results_pp=100
        self.print_img_filenames =False
        self.debug = False
        self.iterations = iterations
        self.last_row_scraped = 0     #Last Row Scraped; camera number to start at.
        self.snapshots_per_camera = 5
        self.seconds_between_snapshots = 3
        self.cycles_completed = 0
        self.cycle_termination_number = 3 #End scraper after this number of completed cycles.
        proj_dir = os.getcwd()
        print("Project Root Directory:\n{}".format(proj_dir))
        self.proj_dir = proj_dir
        self.headless = headless

        if os.path.exists("images"):
            os.chdir("images")
            img_dir = os.getcwd()
            time.sleep(.5)
        else:
            os.mkdir("images")
            os.chdir("images")
            img_dir = os.getcwd()
            time.sleep(.5)
        print("Image Directory: {}".format(img_dir))
        self.img_dir = img_dir
    
    def launch_scraper(self):
        if sys.platform == 'linux':
            print("Setting Linux Chromedriver options.")
            #sys.path.append('/home/matt/Documents/Projects/rpa_recording/chromedriver-linux64/chromedriver')
            #https://stackoverflow.com/questions/56637973/how-to-fix-selenium-devtoolsactiveport-file-doesnt-exist-exception-in-python
            # opts = Options()
            # opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            # opts.add_argument('SEC-CH-UA="Chromium";v="115", "Not/A)Brand";v="99"')


            chromeOptions = webdriver.ChromeOptions() 
            chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
            chromeOptions.add_argument("--no-sandbox") 
            chromeOptions.add_argument("--disable-setuid-sandbox") 

            chromeOptions.add_argument("--remote-debugging-port=9222")  # this

            #chromeOptions.add_argument("--disable-dev-shm-using") 
            #chromeOptions.add_argument("--disable-extensions") 
            #chromeOptions.add_argument("--disable-gpu") 
            chromeOptions.add_argument("start-maximized") 
            chromeOptions.add_argument("disable-infobars")
            #chromeOptions.add_argument(r"user-data-dir=.\cookies\\test")
            if self.headless:
                chromeOptions.add_argument("--headless");

            chromedriver_path = "/home/matt/Documents/Projects/rpa_recording/chromedriver-linux64/chromedriver"

            # self.driver = webdriver.Chrome(chromedriver_path, options=chromeOptions) 

            # self.driver = webdriver.Firefox(self.geckoDriverPath)
            #https://stackoverflow.com/questions/76428561/typeerror-webdriver-init-got-multiple-values-for-argument-options
            service = Service(executable_path="/home/matt/Documents/Projects/rpa_recording/chromedriver-linux64/chromedriver") #Updated Selenium 4.1
            chromedriver_path = "/home/matt/Documents/Projects/rpa_recording/chromedriver-linux64/chromedriver"
            self.driver = webdriver.Chrome(options=chromeOptions)#, service=service)  #Updated selenium 4.1

        else:
            self.driver = webdriver.Firefox(executable_path=self.geckoDriverPath)
        time.sleep(3)
        self.driver.get("https://webcams.nyctmc.org/cameras-list")
    def get_camera_homepage(self):
        self.driver.get("https://webcams.nyctmc.org/cameras-list")

    def pull_camera_table_details(self):
        """Should be at camera list webpage."""
        body = driver.find_element(By.TAG_NAME, 'body')
        body = body.find_element(By.TAG_NAME, 'body')
        main_div = body.find_element(By.TAG_NAME, 'div')

        app_nav = main_div.find_element(By.TAG_NAME, 'app-navigation')

        # cam_list_pc = main_div.find_element(By.XPATH, "//div[@class='g-view-wrapper g-flex ng-tns-c113-0']") #previous, now seeing c115
        cam_list_pc = find_element(main_div, "g-view-wrapper g-flex ng-tns-c", "class")
        # app_cam_list = div2.find_element(By.TAG_NAME, 'app-camera-list')
        cam_list_pc.get_attribute('class') #g-view-wrapper g-flex ng-tns-c113-0
        cam_list = cam_list_pc.find_element(By.TAG_NAME, 'app-cameras-list')
        tbody = cam_list.find_element(By.TAG_NAME, 'tbody')
        trows = tbody.find_elements(By.TAG_NAME, 'tr')

        table_addresses = []
        for trow in trows:
            a , b = get_address_borough(trow)
            table_addresses.append((a,b))
        df = pd.DataFrame(table_addresses)
        df.columns = ['Address','Borough']
        self.camera_tables.append(df)
    def click_checkboxes(self, addresses):
        assert len(address) <= 9, "Error. Can only select up to 9 cameras at a time."
    def img_add_folder(self, img_address):
        folder = clean_img_address(img_address)
        if os.path.exists(folder):
            os.chdir(folder)
        else:
            os.mkdir(folder)
            os.chdir(folder)
        self.folder = folder
        if self.debug:
            print("In folder: ", folder)

    def save_image(self, selenium_img_obj):
        time_now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M_%S")
        img_filename = "{}_{}.png".format(self.folder, time_now)
        if self.print_img_filenames:
            sys.stdout.write("\rSaving to: {}".format(img_filename))
        #Save
        # selenium_img_obj.screenshot(img_filename) #Previously
        src = selenium_img_obj.get_attribute('src')
        # download the image
        urllib.request.urlretrieve(src, img_filename)
        if self.debug:
            print("Saving image: ", img_filename)

    def scrape_images(self):
        driver = self.driver
        proj_dir = self.proj_dir
        img_dir = self.img_dir
        #Get Camera Preview Element
        cam_preview = driver.find_element(By.TAG_NAME, 'app-dialog-camera-preview')
        #Get Grid
        cam_grid = cam_preview.find_element(By.CLASS_NAME,'cameras-grid')
        cam_previews = cam_grid.find_elements(By.TAG_NAME, 'app-camera-view')
        if len(cam_previews)==1:
            #print("Only one camera.")
            img_address = cam_preview.text.split("\n")[0]
            #print(img_address)
            
            cam_n_preview = cam_previews[0]
            imgs = cam_n_preview.find_elements(By.TAG_NAME, 'img')
            cam_img = [i for i in imgs if 'watermark' not in i.get_attribute('class')][0]
            #Folder Structure
            self.img_add_folder(img_address)
            #Save
            self.save_image(cam_img)
            os.chdir(img_dir)
        else:
            for cam_n_preview in cam_previews:
                #Print address
                img_address = cam_n_preview.text.split("\n")[0]
                print(img_address)
                imgs = cam_n_preview.find_elements(By.TAG_NAME, 'img')
                cam_img = [i for i in imgs if 'watermark' not in i.get_attribute('class')][0]
                #Folder Structure
                self.img_add_folder(img_address)
                #Save
                self.save_image(cam_img)
                #Return to Root Folder
                os.chdir(img_dir)
    def set_results_pp(self):
        driver = self.driver
        results_pp = self.results_pp
        body = driver.find_element(By.TAG_NAME, 'body')
        body = body.find_element(By.TAG_NAME, 'body')
        main_div = body.find_element(By.TAG_NAME, 'div')

        app_nav = main_div.find_element(By.TAG_NAME, 'app-navigation')

        #cam_list_pc = main_div.find_element(By.XPATH, "//div[@class='g-view-wrapper g-flex ng-tns-c113-0']")
        # cam_list_pc = main_div.find_element(By.XPATH, "//div[@class='g-view-wrapper g-flex ng-tns-c113-0']") #previous, now seeing c115
        cam_list_pc = find_element(main_div, "g-view-wrapper g-flex ng-tns-c", "class")
        mat_paginator = cam_list_pc.find_element(By.TAG_NAME, 'mat-paginator')
        # pag_outer = cam_list_pc.find_element(By.CLASS_NAME,"mat-paginator-outer-container")
        mat_p_div = mat_paginator.find_element(By.TAG_NAME, 'div')
        mpdiv2 = mat_p_div.find_element(By.CLASS_NAME,"mat-paginator-container")

        arrow = find_element(mpdiv2, "mat-select-arrow", "class")
        arrow.click()
        time.sleep(2)
        
        select_panel = driver.find_element(By.ID,"mat-select-0-panel")
        items_pp_options = select_panel.find_elements(By.TAG_NAME, 'mat-option')
        for item in items_pp_options:
            #print(item.text)
            if item.text == str(results_pp):
                item.click()
        #Check Tot Cam # and Current Results Displayed
        cur_display_n_text = mpdiv2.find_element(By.CLASS_NAME,"mat-paginator-range-label").text
        disp_r_min, disp_r_max, tot_cams = re.findall("(\d+) – (\d+) of (\d+)", cur_display_n_text)[0]
        #print(disp_r_min, disp_r_max, tot_cams)
        self.disp_r_min = int(disp_r_min)
        self.disp_r_max = int(disp_r_max)
        self.tot_cams = int(tot_cams)

    def click_next_page(self):
        driver = self.driver
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        next_page = [b for b in buttons if "Next page" == b.get_attribute('aria-label')][0]
        next_page.click()
    def run(self):
        self.launch_scraper()
        driver = self.driver
        dfs = []
        print("Starting on: {}".format(self.last_row_scraped))
        #page_n = 0 #No Longer Needed #Create counter to keep track of current page.
        for scrape_set in range(self.iterations):
            page_n = (self.last_row_scraped // self.results_pp)
            driver.refresh()
            time.sleep(4)
            self.set_results_pp() #this can crash occassionally when "another element obscures it...."
            for i in range(page_n):
                self.click_next_page()
                time.sleep(np.random.uniform(.85,1.25))
            time.sleep(3)
            #Get Element Selections
            body = driver.find_element(By.TAG_NAME, 'body')
            body = body.find_element(By.TAG_NAME, 'body')
            main_div = body.find_element(By.TAG_NAME, 'div')

            app_nav = main_div.find_element(By.TAG_NAME, 'app-navigation')

            # cam_list_pc = main_div.find_element(By.XPATH, "//div[@class='g-view-wrapper g-flex ng-tns-c113-0']") #previous, now seeing c115
            cam_list_pc = find_element(main_div, "g-view-wrapper g-flex ng-tns-c", "class")
            # app_cam_list = div2.find_element(By.TAG_NAME, 'app-camera-list')
            cam_list_pc.get_attribute('class') #g-view-wrapper g-flex ng-tns-c113-0
            cam_list = cam_list_pc.find_element(By.TAG_NAME, 'app-cameras-list')
            tbody = cam_list.find_element(By.TAG_NAME, 'tbody')
            trows = tbody.find_elements(By.TAG_NAME, 'tr')

            table_addresses = []
            for trow in trows:
                cb_cell , a , b = get_address_borough(trow)
                table_addresses.append((a,b))
            #Format as DataFrame (like excel spreadsheet)
            df = pd.DataFrame(table_addresses)
            df.columns = ['Address','Borough']


            start = self.last_row_scraped % int(self.results_pp)
            if self.debug:
                padding = " "*20
                sys.stdout.write("\rStart: {} Total rows: {}{}".format(start, len(trows),padding))
            n_to_check = 9
            #Update Below to a simple list slice.
            for i, trow in enumerate(trows):
                cb_cell , a , b = get_address_borough(trow)
                if i in range(start, start+n_to_check):
                    checkbox = cb_cell.find_element(By.TAG_NAME, 'mat-checkbox')
                    checkbox.click()
                    self.last_row_scraped += 1
            time.sleep(1.5)
            
            button = cam_list.find_element(By.TAG_NAME, 'button')
            button.click()
            
            time.sleep(3.5)
            #Get 10 images, one every 2 seconds.
            for i in range(self.snapshots_per_camera):
                self.scrape_images()
                time.sleep(self.seconds_between_snapshots)
            #Once all cameras scraped, repeat!
            if self.last_row_scraped >= self.tot_cams:
                self.last_row_scraped = 0
                print("Completed Scraping all Cameras!!")
                self.cycles_completed += 1
            if self.cycles_completed >= self.cycle_termination_number:
                print("Scraping completed. Exiting.")
                return None


if __name__ == '__main__':
    ##To Do: Add argparse
    scraper = camScraper(headless=True, iterations=5*10**3)

    #Update Gecko Driver Path for Ubuntu Desktop
    if sys.platform == 'linux':
        scraper.geckoDriverPath = "/home/matt/Documents/Tools/Scraping/"
    else:
        pass

    print("GeckoDriverPath: {}".format(scraper.geckoDriverPath))
    #scraper.print_img_filenames = True
    scraper.debug = False
    scraper.last_row_scraped = np.random.choice(600)
    print("Last row scraped: {}".format(scraper.last_row_scraped))
    scraper.run()