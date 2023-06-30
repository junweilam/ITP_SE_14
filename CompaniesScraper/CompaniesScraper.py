from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import os

import time

opts = Options()
opts.add_argument("Mozilla/5.0")
driver = webdriver.Chrome(options=opts)
time.sleep(2)

# Starting Point
url_login = 'https://www.glassdoor.sg/index.htm'
url_main = 'https://www.glassdoor.sg/Reviews/index.htm'

# Variables
COUNTRY = 'Singapore'
NGOs = []

# Filter 
c1 = '&locId=167&locType=N&locName=Oman&industry=200016,200018,200044,200045,200059,200087,200088,200089&filterType=RATING_OVERALL'
c2 = '&locId=177&locType=N&locName=Nigeria&industry=200016,200018,200044,200045,200059,200087,200088,200089&filterType=RATING_OVERALL'
c3 = '&locId=3934727&locType=C&locName=Skopje%20(Republic%20of%20Macedonia)&industry=200016,200018,200044,200045,200059,200087,200088,200089&filterType=RATING_OVERALL'
c4 = '&locId=180&locType=N&locName=Norway&industry=200016,200018,200044,200045,200059,200087,200088,200089&filterType=RATING_OVERALL'

# grantmaking = '&locId=240&locType=N&locName=Taiwan&industry=200087&filterType=RATING_OVERALL'
# civic = '&locId=240&locType=N&locName=Taiwan&industry=200089&filterType=RATING_OVERALL'
# religious = '&locId=240&locType=N&locName=Taiwan&industry=200088&filterType=RATING_OVERALL'
# culture = '&locId=240&locType=N&locName=Taiwan&industry=200016&filterType=RATING_OVERALL'

def logIn():
    driver.get(url_login)
    driver.maximize_window()
    name = "email"
    pw = "password"
    try:
        username = driver.find_element(By.ID, 'inlineUserEmail')
        button = driver.find_element(
            By.XPATH, '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/form/div[2]/button')
        username.send_keys(name)
        button.click()
        time.sleep(3)
        password = driver.find_element(By.ID, 'inlineUserPassword')
        password.send_keys(pw)
        sign_in = driver.find_element(
            By.XPATH, '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/form/div[4]/button/span')
        sign_in.click()
        time.sleep(2)
    except:
        time.sleep(2)
        pass

def scrapeCompaniesByCountry(countryName):
    driver.get(url_main)
    location = driver.find_element(By.XPATH, '//*[@id="sc.location"]')
    location.send_keys(countryName)
    search = driver.find_element(By.XPATH, '//*[@id="scBar"]/div/button/span')
    search.click()
    time.sleep(2)

def scraping_pages(num_pages, filter):
    #url_root = driver.current_url.split(".htm")[0]
    url_root = 'https://www.glassdoor.sg/Reviews/index.htm?overall_rating_low=1&page='
    nums = [x+1 for x in range(num_pages)]
    url_mains = list(map(lambda n: url_root + str(n) + filter, nums))
    

    for u in url_mains:
        driver.get(u)
        time.sleep(2)
        elems = driver.find_elements(By.TAG_NAME, 'a')
        print(f'---------------------------------\nPage {u}\n---------------------------------')

        company_links = []

        for elem in elems:
            company_link = elem.get_attribute('href')
            try:
                if company_link.find('Salary') != -1 and company_link is not None and company_link not in company_links:
                    company_links.append(company_link)
            except:
                pass
        
        for url in company_links:
            driver.get(url)
            ov_elems = driver.find_elements(By.TAG_NAME, 'a')
            time.sleep(2)
            for ov_elem in ov_elems:
                ov_link = ov_elem.get_attribute('href')
                code = driver.current_url.split('-E')[1].split('.')[0]
                try:
                    if 'Overview' in ov_link and ov_link is not None and code in ov_link:
                        new_ov_link = ov_link   
                except:
                    pass
            print(f'{new_ov_link}')
            driver.get(new_ov_link)
            time.sleep(2)
            try:
                try:
                    companyType = driver.find_element(By.XPATH, '//*[@id="MainContent"]/div[1]/ul/li[5]/div').text
                except:
                    pass

                if companyType == "":
                    try:
                        companyType = driver.find_element(By.XPATH, '//*[@id="MainContent"]/div[1]/ul/li[4]/div').text
                    except:
                        pass

                companyName = driver.find_element(By.XPATH, '//*[@id="Container"]/div[1]/div[1]/div/div/div[1]/div[5]/div/div[1]/div[2]/div/h1').text
                companyCode = driver.current_url.split('_IE')[1].split('.')[0]
                companyIndustry = driver.find_element(By.XPATH, '//*[@id="MainContent"]/div[1]/ul/li[6]/a').get_attribute("innerText")
                print(f'Company Name: {companyName}\nCompany Type: {companyType}\nCompany Code: {companyCode}\nCompany Industry: {companyIndustry}\n---------------------------------------')
                if companyType == 'Hospital' or companyType == 'Nonprofit Organization' or companyType == 'Non-profit Organisation' or companyType == 'College / University' or companyIndustry == 'Grantmaking & Charitable Foundations':
                    NGOs.append({
                        companyName:{
                            "company_code": companyCode,
                            "company_name": companyName,
                            "Reviews": "No",
                            "Interviews": "No"
                        }
                    })
                companyType = ""
            except:
                pass
    


logIn()

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Scraping Company 1
scraping_pages(6, c1)
with open(os.path.join(location,'Oman.json'), 'w') as fp:
    json.dump(NGOs, fp)

#Scraping Company 2
scraping_pages(61, c2)
with open(os.path.join(location,'Nigeria.json'), 'w') as fp:
    json.dump(NGOs, fp)

#Scraping Company 3
scraping_pages(2, c3)
with open(os.path.join(location,'North Macedonia.json'), 'w') as fp:
    json.dump(NGOs, fp)

#Scraping Company 4
scraping_pages(7, c4)
with open(os.path.join(location,'Norway.json'), 'w') as fp:
    json.dump(NGOs, fp)

#Scraping Grantmaking & Charitable Foundations
# scraping_pages(1, grantmaking)
# with open('D:\\CompaniesScraper\\Taiwan\\Taiwan2.json', 'w') as fp:
#     json.dump(NGOs, fp)

#Scraping Civic & Social Services
# scraping_pages(3, civic)
# with open('D:\\CompaniesScraper\\Taiwan\\Taiwan3.json', 'w') as fp:
#     json.dump(NGOs, fp)

# #Scraping Religious Instituitions
# scraping_pages(1, religious)
# with open('D:\\CompaniesScraper\\Taiwan\\Taiwan3.json', 'w') as fp:
#     json.dump(NGOs, fp)

# #Scraping Culture & Entertainment
# scraping_pages(1, culture)
# with open('D:\\CompaniesScraper\\Taiwan\\Taiwan3.json', 'w') as fp:
#     json.dump(NGOs, fp)

driver.close()
driver.quit()