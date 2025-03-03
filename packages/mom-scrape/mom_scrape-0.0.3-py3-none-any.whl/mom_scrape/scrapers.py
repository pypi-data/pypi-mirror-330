from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

import os
import json
from pathlib import Path
import urllib.request
import shutil
from zipfile import ZipFile
import time
import requests
import re

class WebScraper():
    def __init__(self, dataset_of_interest, website_link):
        self.dataset_of_interest=dataset_of_interest
        self.website_link=website_link
        self.FILETYPE=['xlsx'] # can change to ['zip','csv'] if you want the csv files
        
    def get_info(self):
        # chromedriver_autoinstaller.install(path=".")       
        options = Options()
        options.add_argument('--headless=new') 
        service = ChromeService('chromedriver-mac-arm64/chromedriver')

        # driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
        driver=webdriver.Chrome(options=options)        
        
        driver.get(self.website_link)
        dates_fp=self.website_link.split("/")[-1].split(".")[0]
        
        if not os.path.exists('dates'):
            os.makedirs('dates')
        
        # there is a database containing the dataset and the last updated date of the dataset. the script will scrape the latest 
        # info off the MOM website. if the update date on the website differs from what is stored locally in the database,
        # treat the dataset as updated and send this dataset to designated email address(es)
        if os.path.isfile(f'dates/{dates_fp}.json'):
            with open(f'dates/{dates_fp}.json', 'r') as fp:
                old_dates = json.load(fp)
        else:
            old_dates={}
            
        results={}
        dates={}
        
        trs = driver.find_elements(By.XPATH, "//tr")
         
        # on MOM's website, go row by row and retrieve relevant info from each row, which are (1) name of dataset,
        # (2) updated date of dataset and (3) links to download the dataset
        for tr in trs:
            # table row doesnt have arrowlink
            try:
                label=tr.find_element(By.CLASS_NAME, 'arrowlink').text.encode('ascii', 'ignore').decode("utf-8")
            except NoSuchElementException:
                continue
            
            if label not in self.dataset_of_interest:
                continue
            
            
            
            links1=tr.find_elements(By.CSS_SELECTOR, ".filetype [href]")
            links2=tr.find_elements(By.CSS_SELECTOR, ".size  [href]")
            links=links1+links2
            
            links=[link.get_attribute('href') for link in links]
            
            # filter to get right file type
            links=[link for link in links if link.split(".")[-1] in self.FILETYPE]
            
            # get date updated
            # date=tr.find_element(By.CSS_SELECTOR, "div[style='padding-left:20px;']").text
            date=tr.text
            date = re.search(r"(Released on: \d{1,2} \w+ \d{4})", date).group(1)
            
            # if the file has not been loaded before OR date has been updated
            old_date=old_dates.get(label, 'missing')
            if (old_date =='missing') or (date != old_date):
                if len(links)>1:
                    raise Exception(f"More than 1 file to download, offending line is {label}")
                
                if len(links)==0:
                    print(f"{label} is dropped because no file found")
                else:
                    results[label]=links[0]
                
                dates[label]=date

        # update old dates with new dates
        old_dates.update(dates)

        # if there are new datasets, then continue with the rest of the script
        if results:
            print(f'the following stats have been updated: {results.keys()}')
            
            with open(f'dates/{dates_fp}.json', 'w') as fp:
                json.dump(old_dates, fp)
                
            parent=Path('stats')
            parent.mkdir(exist_ok=True)
                
            [dl_and_save(file_name, link, parent) for (file_name, link) in results.items()]
            
            # Transfer the downloaded updated datasets into a zip file, to be attached in the email
            with ZipFile('stats.zip', 'w') as zip_object:
                for folder_name, sub_folders, file_names in os.walk(parent):
                    for filename in file_names:
                        if filename.split('.')[0] in results:
                            file_path = os.path.join(folder_name, filename)
                            zip_object.write(file_path, os.path.basename(file_path))
        return results                
                
def dl_and_save(file_name, link, parent):
    """download and save files locally

    Args:
        file_name (str): file name of dataset
        link (str): html link to donwload dataset
    """
    filetype=link.split(".")[-1]
    file_name=parent/(file_name+f'.{filetype}')
    with urllib.request.urlopen(link) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

class ReportScraper():
    def __init__(self, filter_by='Reports', save_dir='stats/reports'):
        self.filter_by=filter_by
        self.save_dir=Path(save_dir)
        
    def get_dates(self):
        if not os.path.exists('dates'):
            os.makedirs('dates')
            
        if os.path.isfile(f'dates/mom_reports.json'):
            with open(f'dates/mom_reports.json', 'r') as fp:
                old_dates = json.load(fp)
        else:
            old_dates={}
        return old_dates
        
        
    def get_info(self):
        old_dates=self.get_dates()
        new_dates={}
        results=[]
        
        options=Options()
        # options.add_argument('--headless=new') 
        # service = ChromeService('chromedriver-mac-arm64/chromedriver')

        driver=webdriver.Chrome(options=options)           
        
        driver.get('https://stats.mom.gov.sg/Publications/Pages/Publications.aspx')

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-control.alltypes"))
            )
        select_element = driver.find_element(By.CLASS_NAME, 'form-control.alltypes')
        
        select = Select(select_element)
        select.select_by_value('Articles')
        select.select_by_value(self.filter_by)
        
        if os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
        os.makedirs(self.save_dir)
            
        trs = driver.find_elements(By.XPATH, "//tr")
        for tr in trs:
            try:
                my_element_name = 'title'
                ignored_exceptions=(StaleElementReferenceException)
                WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions)\
                    .until(EC.presence_of_element_located((By.CLASS_NAME, my_element_name)))
                title=tr.find_element(By.CLASS_NAME, 'title').text                
                title=title.replace("Report: ", "")
                print(title)

                date=tr.find_element(By.CLASS_NAME, 'date').text
                download_link=tr.find_element(By.CLASS_NAME, 'attachfile').get_attribute('href')
            except NoSuchElementException:
                continue
                        
            # if report hasnt been seen before/ has been updated
            if old_dates.get(title, 'missing') != date:          
                filename = (self.save_dir/title).with_suffix('.pdf')
                response = requests.get(download_link)
                filename.write_bytes(response.content)
                
                new_dates[title]=date
                results.append(filename)
                
        if new_dates:
            old_dates.update(new_dates)
            
        if results:
            print(f'the following reports have been updated: {results}')
            
            with open(f'dates/mom_reports.json', 'w') as fp:
                json.dump(old_dates, fp)
                
        else:
            print('no new report')
            
        return results
        

if __name__=="__main__":
    test=ReportScraper()
    test.get_info()

