from GenericDriver import FireFoxWebDriver
from GenericDriver import ChromeWebDriver
from GlassDoorScraper import GlassDoorScraper
from GlassDoorReviewWorker import GlassDoorReviewWorker
from GlassDoorInterviewWorker import GlassDoorInterviewWorker
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

def main():
    # Modify company_code, company_name and account_number (see accounts.json)
    # e.g., for Visa - https://www.glassdoor.sg/Overview/Working-at-Visa-Inc-EI_IE3035.11,19.htm
    # e.g., Company_name = Visa, Company_code = 3035
    company_code =  3046
    company_name = "YMCA"


    # Will be resolved to Facebook_{account_number} in accounts.json. 
    account_number = 1

    # will scrape 100 urls (1000 reviews) before dumping results to json
    batch_size = 100 

    # Create review worker object to start scraping for reviews
    review_worker = GlassDoorReviewWorker(company_code, company_name, account_number, batch_size)
    
    """Uncomment to scrape one company: i.e., scrape the company_code and company_name provided above"""
    #review_worker.start_one_scrape()

    """Uncomment if you want to resume a scrape that terminated prematurely"""
    # review_worker.resume_scrape()

    """Uncomment if you want to scrape multiple companies. (Provide this json file in FILE_PATH)"""
    FILE_PATH = os.path.join(".", "Companies", "United States College.json") # Modify this
    review_worker.start_multiple_scrapes(FILE_PATH) 

    # interview_worker = GlassDoorInterviewWorker(company_code, company_name, account_number, batch_size)

    # FILE_PATH = os.path.join(".", "Companies", "Singapore.json") # Modify this
    # interview_worker.start_multiple_scrapes_interview(FILE_PATH) 
    # interview_worker.start_one_scrape_interview()

if __name__ == "__main__":
  main()
