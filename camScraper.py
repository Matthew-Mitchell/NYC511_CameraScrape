#Must Haves
from selenium import webdriver
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

proj_dir = os.getcwd()
print("Project Root Directory:\n{}".format(proj_dir))

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

def clean_img_address(a):
    a = a.replace(" ","_")
    a = a.replace("@","at")
    a = a.replace("/","_")
    a = a.replace(".","")
    return a

def find_element(containing_el, search_term, attribute):
    n_el = 0
    needle = None
    for el in containing_el.find_elements_by_xpath(".//*"):
        n_el += 1
        att_value = el.get_attribute(attribute)
        if att_value:
            if search_term in att_value:
                needle = el
                return needle
def get_address_borough(trow):
    cb_cell, a_cell, b_cell =  trow.find_elements_by_tag_name('td')[:3]
    return (cb_cell, a_cell.text, b_cell.text)

def parse_row_text(row_text):
    boroughs = ['Manhattan','Bronx','Staten Island','Queens','Brooklyn']
    borough = [b for b in boroughs if b in row_text][0]
    address = row_text.replace(borough,"")
    return address, borough

class camScraper:
    def __init__(self, iterations=10**3, last_row_scraped=0):
        self.geckoDriverPath = '/Users/matthewmitchell/Documents/Projects/Tools/Python/Scraping/geckodriver'
        self.camera_tables = []
        self.results_pp=100
        self.print_img_filenames =False
        self.debug = False
        self.iterations = iterations
        self.last_row_scraped = 850     #Last Row Scraped; camera number to start at.    
        pass
    def launch_scraper(self):
        self.driver = webdriver.Firefox(executable_path=self.geckoDriverPath)
        time.sleep(3)
        self.driver.get("https://webcams.nyctmc.org/cameras-list")
    def get_camera_homepage(self):
        self.driver.get("https://webcams.nyctmc.org/cameras-list")

    def pull_camera_table_details(self):
        """Should be at camera list webpage."""
        body = driver.find_element_by_tag_name('body')
        body = body.find_element_by_tag_name('body')
        main_div = body.find_element_by_tag_name('div')

        app_nav = main_div.find_element_by_tag_name('app-navigation')

        cam_list_pc = main_div.find_element_by_xpath("//div[@class='g-view-wrapper g-flex ng-tns-c113-0']")
        # app_cam_list = div2.find_element_by_tag_name('app-camera-list')
        cam_list_pc.get_attribute('class') #g-view-wrapper g-flex ng-tns-c113-0
        cam_list = cam_list_pc.find_element_by_tag_name('app-cameras-list')
        tbody = cam_list.find_element_by_tag_name('tbody')
        trows = tbody.find_elements_by_tag_name('tr')

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

    def save_image(self, selenium_img_obj):
        time_now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M_%S")
        img_filename = "{}_{}.png".format(self.folder, time_now)
        if self.print_img_filenames:
            sys.stdout.write("\rSaving to: {}".format(img_filename))
        #Save
        selenium_img_obj.screenshot(img_filename)
    def scrape_images(self):
        driver = self.driver
        #Get Camera Preview Element
        cam_preview = driver.find_element_by_tag_name('app-dialog-camera-preview')
        #Get Grid
        cam_grid = cam_preview.find_element_by_class_name('cameras-grid')
        cam_previews = cam_grid.find_elements_by_tag_name('app-camera-view')
        if len(cam_previews)==1:
            print("Only one camera.")
            img_address = cam_preview.text.split("\n")[0]
            print(img_address)
            
            cam_n_preview = cam_previews[0]
            imgs = cam_n_preview.find_elements_by_tag_name('img')
            cam_img = [i for i in imgs if 'watermark' not in i.get_attribute('class')][0]
            #Folder Structure
            scraper.img_add_folder(img_address)
            #Save
            scraper.save_image(cam_img)
            os.chdir(img_dir)
        else:
            for cam_n_preview in cam_previews:
                #Print address
                img_address = cam_n_preview.text.split("\n")[0]
                print(img_address)
                imgs = cam_n_preview.find_elements_by_tag_name('img')
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
        body = driver.find_element_by_tag_name('body')
        body = body.find_element_by_tag_name('body')
        main_div = body.find_element_by_tag_name('div')

        app_nav = main_div.find_element_by_tag_name('app-navigation')

        cam_list_pc = main_div.find_element_by_xpath("//div[@class='g-view-wrapper g-flex ng-tns-c113-0']")
        mat_paginator = cam_list_pc.find_element_by_tag_name('mat-paginator')
        # pag_outer = cam_list_pc.find_element_by_class_name("mat-paginator-outer-container")
        mat_p_div = mat_paginator.find_element_by_tag_name('div')
        mpdiv2 = mat_p_div.find_element_by_class_name("mat-paginator-container")

        arrow = find_element(mpdiv2, "mat-select-arrow", "class")
        arrow.click()
        time.sleep(2)
        
        select_panel = driver.find_element_by_id("mat-select-0-panel")
        items_pp_options = select_panel.find_elements_by_tag_name('mat-option')
        for item in items_pp_options:
            #print(item.text)
            if item.text == str(results_pp):
                item.click()
        #Check Tot Cam # and Current Results Displayed
        cur_display_n_text = mpdiv2.find_element_by_class_name("mat-paginator-range-label").text
        disp_r_min, disp_r_max, tot_cams = re.findall("(\d+) – (\d+) of (\d+)", cur_display_n_text)[0]
        #print(disp_r_min, disp_r_max, tot_cams)
        self.disp_r_min = int(disp_r_min)
        self.disp_r_max = int(disp_r_max)
        self.tot_cams = int(tot_cams)

    def click_next_page(self):
        driver = self.driver
        buttons = driver.find_elements_by_tag_name('button')
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
            time.sleep(3)
            self.set_results_pp() #this can crash occassionally when "another element obscures it...."
            for i in range(page_n):
                self.click_next_page()
                time.sleep(np.random.uniform(.5,.75))
            time.sleep(3)
            #Get Element Selections
            body = driver.find_element_by_tag_name('body')
            body = body.find_element_by_tag_name('body')
            main_div = body.find_element_by_tag_name('div')

            app_nav = main_div.find_element_by_tag_name('app-navigation')

            cam_list_pc = main_div.find_element_by_xpath("//div[@class='g-view-wrapper g-flex ng-tns-c113-0']")
            # app_cam_list = div2.find_element_by_tag_name('app-camera-list')
            cam_list_pc.get_attribute('class') #g-view-wrapper g-flex ng-tns-c113-0
            cam_list = cam_list_pc.find_element_by_tag_name('app-cameras-list')
            tbody = cam_list.find_element_by_tag_name('tbody')
            trows = tbody.find_elements_by_tag_name('tr')

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
                    checkbox = cb_cell.find_element_by_tag_name('mat-checkbox')
                    checkbox.click()
                    self.last_row_scraped += 1
            time.sleep(1.5)
            
            button = cam_list.find_element_by_tag_name('button')
            button.click()
            
            time.sleep(3.5    )
            #Get 10 images, one every 2 seconds.
            for i in range(10):
                self.scrape_images()
                time.sleep(2)
            #Once all cameras scraped, repeat!
            if self.last_row_scraped >= self.tot_cams:
                self.last_row_scraped = 0
                print("Completed Scraping all Cameras!!")
