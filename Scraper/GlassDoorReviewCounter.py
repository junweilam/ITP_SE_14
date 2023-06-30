from GenericDriver import FireFoxWebDriver
from GenericDriver import ChromeWebDriver
from GlassDoorScraper import GlassDoorScraper

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
import sys 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import numpy as np 
import os 
import json 

Counter =[]
COUNTRY ="Singapore Review Counts"
class GlassDoorReviewCounter:
    def __init__(self, company_code, company_name, account_number, batch_size):
        self.company_code = company_code
        self.company_name = company_name
        self.account_number = account_number
        self.batch_size = batch_size
        self.list_of_review_pages = []
        self.reviews_collected = []
        self.list_of_interview_pages = []
        self.interviews_collected = []
        self.batch_counter = 0
        self.worker = self.create_worker() # Aggregation

    def create_worker(self):
        """Creates 1 worker, that will be used to scrape glassdoor"""
        account_type = f"Facebook_{self.account_number}"
        try:
            worker = GlassDoorScraper(driver=ChromeWebDriver(), company_code=self.company_code, company_name=self.company_name)
            worker.login_using_facebook(account_type=account_type)
        except InvalidSessionIdException:
            print(f"Failed to login using {account_type} - Blocked by captcha.")
            sys.exit(1)
        return worker

    def generate_urls(self):
        """Generates a list of urls to scrape"""
        Counter.append({
                        self.company_name:{
                            "Review Count": self.worker.generate_reviews_Count(),
                        }
                    }) 
    
    # def generate_urls_interview(self):
    #     """Generates a list of urls to scrape"""
    #     self.list_of_interview_pages = self.worker.generate_interview_urls()

    def start_one_scrape(self):
        """ Scrape one company for reviews """
        self.generate_urls()
        print(f"getting Review Count for {self.company_name}...")
    
    def start_multiple_scrapes(self, file_path):
        """Scrapes multiple companies for reviews."""
        # Read json containing company codes and list
        try:
            with open(file_path) as f:
                json_data = json.load(f)
                # Extract code and name
                for item in json_data:
                    for company, company_info in item.items():
                        self.company_code = company_info['company_code']
                        self.company_name = company_info['company_name']
                        self.worker.company_code = self.company_code
                        self.worker.company_name = self.company_name
                        self.batch_counter = 0
                        self.start_one_scrape()

            location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

            with open(os.path.join(location,COUNTRY+'.json'), 'w') as fp:
                json.dump(Counter, fp)

        except FileNotFoundError:
            print(f"Error: {file_path} provided does not exist. Exiting.")
            print("Please ensure that you are in the scraper directory")
            sys.exit(1)


     

