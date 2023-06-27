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

class camScraper:
	def __init__(self):
		self.geckoDriverPath = '/Users/matthewmitchell/Documents/Projects/Tools/Python/Scraping/geckodriver'
		self.camera_tables = []
		pass
	def launch_scraper(self):
		self.driver = webdriver.Firefox(executable_path=self.geckoDriverPath)
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
