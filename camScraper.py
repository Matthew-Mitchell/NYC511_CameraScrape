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

def clean_img_address(a):
    a = a.replace(" ","_")
    a = a.replace("@","at")
    a = a.replace("/","_")
    a = a.replace(".","")
    return a

def img_add_folder(img_address):
    folder = clean_img_address(img_address)
    if os.path.exists(folder):
        os.chdir(folder)
    else:
        os.mkdir(folder)
        os.chdir(folder)

def save_image(selenium_img_obj, to_print=False):
    time_now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M_%S")
    img_filename = "{}_{}.png".format(folder, time_now)
    if to_print:
        print("Saving to: ", img_filename)
    #Save
    selenium_img_obj.screenshot(img_filename)

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
    def __init__(self):
        self.geckoDriverPath = '/Users/matthewmitchell/Documents/Projects/Tools/Python/Scraping/geckodriver'
        self.camera_tables = []
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
    def scrape_images(self, proj_dir):
        driver = self.driver
        #Get Camera Preview Element
        cam_preview = driver.find_element_by_tag_name('app-dialog-camera-preview')
        #Get Grid
        cam_grid = cam_preview.find_element_by_class_name('cameras-grid')
        cam_previews = cam_grid.find_elements_by_tag_name('app-camera-view')
        for cam_n_preview in cam_previews:
            #Print address
            img_address = cam_n_preview.text.split("\n")[0]
            print(img_address)
            imgs = cam_n_preview.find_elements_by_tag_name('img')
            cam_img = [i for i in imgs if 'watermark' not in i.get_attribute('class')][0]
            #Folder Structure
            img_add_folder(img_address)
            #Save
            save_image(cam_img, to_print=True)
            #Return to Root Folder
            os.chdir(proj_dir)
    def set_results_pp(self, results_pp="100"):
        driver = self.driver
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
            if item.text == "100":
                item.click()
    def click_next_page(self):
        driver = self.driver
        buttons = driver.find_elements_by_tag_name('button')
        next_page = [b for b in buttons if "Next page" == b.get_attribute('aria-label')][0]
        next_page.click()
    def run(self):
        self.launch_scraper()
        driver = self.driver
        dfs = []
        last_row_scraped = 0
        for scrape_set in range(10):
            driver.refresh()
            time.sleep(2)
            self.set_results_pp()
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


            start = last_row_scraped
            n_to_check = 9
            for i, trow in enumerate(trows):
                cb_cell , a , b = get_address_borough(trow)
                if i in range(start, start+n_to_check):
                    checkbox = cb_cell.find_element_by_tag_name('mat-checkbox')
                    checkbox.click()
                    last_row_scraped += 1
            time.sleep(1.5)
            
            button = cam_list.find_element_by_tag_name('button')
            button.click()
            
            time.sleep(2)
            self.scrape_images(driver, proj_dir)
            time.sleep(20)
