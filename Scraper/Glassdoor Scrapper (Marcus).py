#------------------------------------IMPORTS-------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
#allow time to load
import time
#insert into csv
import pandas as pd
#------------------------------------IMPORTS-------------------------------

#--------------------------------EDITING VARIABLES ------------------------------
#As glassdoor is not as simple as linkedin, you must copy the whole URL
COMPANY_URL = "https://www.glassdoor.sg/Overview/Working-at-Amazon-EI_IE6036.11,17.htm"
#OPTIONS:
# Overview -> 1
# Review -> 2
# Interviews -> 5
OPTION = 1

#Enter email for glassdoor
EMAIL = "[enter email here]"

#Enter password for glassdoor
PASSWORD = "[enter password here]"

#SCALE:
# Enter the number of records you want, -1 if you want to scrap till the end, please number it in multiples of 10s
LIMIT = 20

#--------------------------------EDITING VARIABLES ------------------------------

def checkReviewRating(class_name):
    if class_name == "css-1mfncox":
        return 1
    elif class_name == "css-11p3h8x":
        return 2
    elif class_name == "css-k58126":
        return 3
    elif class_name == "css-94nhxw":
        return 4
    elif class_name == "css-11w4osi":
        return 5
    else:
        return 0

def checkRecommendation(class_name):
    if "css-hcqxoa" in class_name:
        return "Yes"
    elif "css-1h93d4v" in class_name:
        return "Neutral"
    elif "css-1kiw93k" in class_name:
        return "No"
    else:
        return None

def checkBusinessOutlook(class_name):
    if "css-hcqxoa" in class_name:
        return "Good"
    elif "css-1h93d4v" in class_name:
        return "Neutral"
    elif "css-1kiw93k" in class_name:
        return "Bad"
    else:
        return None
    
if __name__ == "__main__":
    #--------------------------------INITIALIZE WEB DRIVER --------------------------------
    #initializing the driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")

    #Uncomment this if you dont want a new chrome window every time
    #options.add_argument('headless')

    #change ath to where chromedriver is in your home folder
    driver = webdriver.Chrome(options=options)
    
    #TO SIGN IN---------------------------------------------------------
    driver.get("https://www.glassdoor.sg/index.htm")
    time.sleep(3)
    driver.find_element(By.ID,"inlineUserEmail").send_keys(EMAIL)
    #click button to procede
    emailButton = driver.find_element(By.CLASS_NAME,"email-button")
    emailButton.click()
    time.sleep(3)
    driver.find_element(By.ID,"inlineUserPassword").send_keys(PASSWORD)
    #click button to procede
    loginButton = driver.find_element(By.CLASS_NAME,"css-8zxfjs")
    loginButton.click()
    time.sleep(3)
    #TO SIGN IN----------------------------------------------------------
    
    driver.get(COMPANY_URL)
    time.sleep(2)
    action = ActionChains(driver)
    #--------------------------------INITIALIZE WEB DRIVER --------------------------------
    company_name = driver.find_element(By.CLASS_NAME,"css-16jzkgq").get_attribute("innerText")
    companyname = []
    companyname.append(company_name.replace(" Overview",''))
    #--------------------------------SCRAP OVERVIEW ---------------------------------------
    if OPTION == 1:
        website = []
        headquarters = []
        size = []
        company_type = []
        industry = []
        revenue = []
        overviews = []
        missions = []
        compeititors = []
        
        overview_details = driver.find_element(By.CLASS_NAME,"css-155za0w").find_elements(By.TAG_NAME,"li")
        for detail in overview_details:
            header = detail.find_element(By.TAG_NAME,"label").get_attribute("innerText")
            if header == "Website:":
                website.append(detail.find_element(By.TAG_NAME,"a").get_attribute("innerText"))
            elif header == "Headquarters:":
                headquarters.append(detail.find_element(By.TAG_NAME,"div").get_attribute("innerText"))
            elif header == "Size:":
                size.append(detail.find_element(By.TAG_NAME,"div").get_attribute("innerText"))
            elif header == "Type:":
                company_type.append(detail.find_element(By.TAG_NAME,"div").get_attribute("innerText"))
            elif header == "Industry:":
                industry.append(detail.find_element(By.TAG_NAME,"a").get_attribute("innerText"))
            elif header == "Revenue:":
                revenue.append(detail.find_element(By.TAG_NAME,"div").get_attribute("innerText"))
        try:
            try:
                readMore = driver.find_element(By.XPATH,"//span[@data-test='employerDescription']/button")
                readMore.click()
            except:
                pass
            overview = driver.find_element(By.XPATH,"//span[@data-test='employerDescription']").get_attribute("innerText")
            overviews.append(overview)
        except:
            overviews.append(None)
            
        try:
            try:
                readMore = driver.find_element(By.XPATH,"//span[@data-test='employerMission']/button")
                readMore.click()
            except:
                pass
            employerMission = driver.find_element(By.XPATH,"//span[@data-test='employerMission']").get_attribute("innerText")
            missions.append(employerMission)
        except:
            missions.append(None)

        #try:
        compeititor = driver.find_element(By.XPATH,"//p[@data-test='employerCompetitors']/span").get_attribute("innerText")
        compeititors.append(compeititor)
        #except:
            #compeititors.append(None)

        
        
        overview_data = pd.DataFrame({'Company':companyname,
                                      'Website':website,
                                      'Headquarters':headquarters,
                                      'Size':size,
                                      'Type':company_type,
                                      'Industry':industry,
                                      'Revenue':revenue,
                                      'Overview':overviews,
                                      'Mission':missions,
                                      'Competitors':compeititors})
        ExcelFileName = companyname[0] + ".xlsx"
        writer = pd.ExcelWriter(ExcelFileName,engine='openpyxl')
        overview_data.to_excel(writer,sheet_name='Overview')
        writer.save()

    #get reviews
    elif OPTION == 2:
        #navigate to review button
        reviewBtn = driver.find_element(By.PARTIAL_LINK_TEXT, 'Reviews')
        reviewBtn.click()
        time.sleep(1)
        
        #INITIALIZE ALL THE LIST HOLY SHIT
        overall_rating=[]
        worklife_rating=[]
        culture_rating=[]
        diversity_rating=[]
        career_rating=[]
        compensation_rating=[]
        senior_rating=[]
        review_title=[]
        employment_status=[]
        date_of_review=[]
        position=[]
        location=[]
        recommended=[]
        ceo_approval=[]
        business_outlook=[]
        pros=[]
        cons=[]

        keepRunning = True
        totalData = 0
        #find the ol element storing all list
        #this try is to store all the data in case of an error
        try:
            while(keepRunning):
                time.sleep(5)
                reviews = driver.find_element(By.CLASS_NAME,"empReviews").find_elements(By.CLASS_NAME,"empReview")
                for review in reviews:
                    #get overall ratings
                    overallRating = review.find_element(By.CLASS_NAME,"ratingNumber").find_element(By.XPATH,"../div").get_attribute("class")
                    overallRating = overallRating.replace(" e1hd5jg10",'')
                    overall_rating.append(checkReviewRating(overallRating))

                    #getting additional ratings
                    try:
                        additionalRatings = review.find_element(By.CLASS_NAME,"tooltipContainer").find_element(By.TAG_NAME,"ul").find_elements(By.TAG_NAME,"li")
                        item = 0
                        wlAdded = False
                        curAdded = False
                        drAdded = False
                        carAdded = False
                        corAdded = False
                        srAdded = False
                        for rating in additionalRatings:
                            reviewHeader = rating.find_element(By.TAG_NAME,"div").get_attribute("innerHTML")
                            rating_class = rating.find_element(By.CLASS_NAME,"e1hd5jg10").get_attribute("class")
                            rating_class = rating_class.replace(" e1hd5jg10",'')
                            if reviewHeader == "Work/Life Balance":
                                wlAdded = True
                                worklife_rating.append(checkReviewRating(rating_class))
                            elif reviewHeader == "Culture &amp; Values":
                                curAdded = True
                                culture_rating.append(checkReviewRating(rating_class))
                            elif reviewHeader == "Diversity and Inclusion":
                                drAdded = True
                                diversity_rating.append(checkReviewRating(rating_class))
                            elif reviewHeader == "Career Opportunities":
                                carAdded = True
                                career_rating.append(checkReviewRating(rating_class))
                            elif reviewHeader == "Compensation and Benefits":
                                corAdded = True
                                compensation_rating.append(checkReviewRating(rating_class))
                            elif reviewHeader == "Senior Management":
                                srAdded = True
                                senior_rating.append(checkReviewRating(rating_class))
                            item+=1
                        if item != 6:
                            if not wlAdded:
                                worklife_rating.append(None)
                            if not curAdded:
                                culture_rating.append(None)
                            if not drAdded:
                                diversity_rating.append(None)
                            if not carAdded:
                                career_rating.append(None)
                            if not corAdded:
                                compensation_rating.append(None)
                            if not srAdded:
                                senior_rating.append(None)
                    except:
                        worklife_rating.append(None)
                        culture_rating.append(None)
                        diversity_rating.append(None)
                        career_rating.append(None)
                        compensation_rating.append(None)
                        senior_rating.append(None)
                    
                    #review name
                    name = review.find_element(By.CLASS_NAME,"reviewLink").get_attribute("innerText")
                    review_title.append(name)

                    #employment Status
                    status = review.find_element(By.CLASS_NAME,"eg4psks0").get_attribute("innerText")
                    employment_status.append(status)

                    #date of review and position
                    DORandP = review.find_element(By.CLASS_NAME,"common__EiReviewDetailsStyle__newGrey").get_attribute("innerText")
                    DORandP = DORandP.split(" - ")
                    date_of_review.append(DORandP[0])
                    position.append(DORandP[1])

                    #location
                    try:
                        locationText = review.find_element(By.CLASS_NAME,"common__EiReviewDetailsStyle__newUiJobLine").find_element(By.XPATH,".//span[@class='middle']").find_element(By.TAG_NAME,"span").get_attribute("innerText")
                        location.append(locationText)
                    except:
                        location.append(None)

                    #recommendation, ceo approval and business outlook
                    company_RCB = review.find_element(By.CLASS_NAME,"reviewBodyCell").find_elements(By.TAG_NAME,"div")
                    count = 0
                    for item in company_RCB:
                        if count == 0:
                            imageType = item.find_element(By.TAG_NAME,"span").get_attribute("class")
                            recommended.append(checkRecommendation(imageType))
                        elif count == 1:
                            imageType = item.find_element(By.TAG_NAME,"span").get_attribute("class")
                            ceo_approval.append(checkRecommendation(imageType))
                        else:
                            imageType = item.find_element(By.TAG_NAME,"span").get_attribute("class")
                            business_outlook.append(checkBusinessOutlook(imageType))
                        count+=1

                    #pros and cons
                    ProsAndCons = review.find_elements(By.CLASS_NAME,"v2__EIReviewDetailsV2__fullWidth")
                    count = 0
                    for item in ProsAndCons:
                        if count == 0:
                            prosText = item.find_element(By.TAG_NAME,"span").get_attribute("innerText")
                            pros.append(prosText)
                        elif count == 1:
                            consText = item.find_element(By.TAG_NAME,"span").get_attribute("innerText")
                            cons.append(consText)
                        else:
                            break
                        count += 1
                totalData += 10
                totalString = str(totalData) + " Reviews Scrapped"
                print(totalString)
                nextBtn = driver.find_element(By.CLASS_NAME,"nextButton")
                #insert to excel file
                time.sleep(3)
                if totalData == LIMIT:
                    keepRunning = False
                if nextBtn.is_enabled():
                    nextBtn.click()
                else:
                    keepRunning = False
            
            #once finished, save to excel
            review_data = pd.DataFrame({'Review Title':review_title,
                                      'Overall Rating':overall_rating,
                                      'Worklife Balance':worklife_rating,
                                      'Culture and Values':culture_rating,
                                      'Diversity and Inclusion':diversity_rating,
                                      'Career Opportunities':career_rating,
                                      'Compensation and Benefits':compensation_rating,
                                      'Senior Management':senior_rating,
                                      'Emloyment Status':employment_status,
                                      'Date of Review':date_of_review,
                                      'Position':position,
                                      'Location':location,
                                      'Recommended':recommended,
                                      'CEO Approval':ceo_approval,
                                      'Business Outlook':business_outlook,
                                      'Pros':pros,
                                      'Cons':cons})
            ExcelFileName = companyname[0] + "_reviews.xlsx"
            writer = pd.ExcelWriter(ExcelFileName,engine='openpyxl')
            review_data.to_excel(writer,sheet_name='Reviews')
            writer.save()
            

        #if it fails still save data
        except Exception as e:
            review_data = pd.DataFrame({'Review Title':review_title,
                                      'Overall Rating':overall_rating,
                                      'Worklife Balance':worklife_rating,
                                      'Culture and Values':culture_rating,
                                      'Diversity and Inclusion':diversity_rating,
                                      'Career Opportunities':career_rating,
                                      'Compensation and Benefits':compensation_rating,
                                      'Senior Management':senior_rating,
                                      'Emloyment Status':employment_status,
                                      'Date of Review':date_of_review,
                                      'Position':position,
                                      'Location':location,
                                      'Recommended':recommended,
                                      'CEO Approval':ceo_approval,
                                      'Business Outlook':business_outlook,
                                      'Pros':pros,
                                      'Cons':cons})
            ExcelFileName = companyname[0] + "_reviews.xlsx"
            writer = pd.ExcelWriter(ExcelFileName,engine='openpyxl')
            review_data.to_excel(writer,sheet_name='Reviews')
            writer.save()
            print(e)
    
    #scrapping interviews
    elif OPTION == 5:
        interviewBtn = driver.find_element(By.PARTIAL_LINK_TEXT, 'Interview')
        interviewBtn.click()
        time.sleep(4)

        dateList=[]
        titles=[]
        results=[]
        experiences=[]
        difficulties=[]
        applicationTypes=[]
        interviewDescriptions=[]
        interviewQuestions=[]
        keepRunning = True
        totalData = 0

        try:
            while(keepRunning):
                time.sleep(3)
                interviews = driver.find_element(By.XPATH,"//div[@data-test='InterviewList']").find_elements(By.CLASS_NAME,"ec4dwm00")
                for interview in interviews:
                    #Get Date
                    dateText = interview.find_element(By.XPATH,".//time[1]").get_attribute("innerHTML")
                    dateList.append(dateText)

                    #get titles
                    titleText = interview.find_element(By.CLASS_NAME,"el6ke055").find_element(By.XPATH,".//a[1]").get_attribute("innerText")
                    titles.append(titleText)

                    #get results
                    #get experiences
                    #get difficulties
                    resultBool = False
                    experienceBool = False
                    difficultyBool = False
                    totalField = interview.find_element(By.CLASS_NAME,"col-12").find_elements(By.CLASS_NAME,"d-sm-inline-block")
                    for field in totalField:
                        field_title = field.find_element(By.XPATH,".//div[1]/span[2]").get_attribute("innerHTML")
                        field_text = field_title.split()
                        if field_text[1] == "Offer":
                            resultBool = True
                            results.append(field_text[0])
                        elif field_text[1] == "Experience":
                            experienceBool = True
                            experiences.append(field_text[0])
                        elif field_text[1] == "Interview":
                            difficultyBool = True
                            difficulties.append(field_text[0])
                    if resultBool == False:
                        results.append(None)
                    if experienceBool == False:
                        experiences.append(None)
                    if difficultyBool == False:
                        difficulties.append(None)
                    
                    try:
                        #get application type
                        applicationText = interview.find_element(By.XPATH,".//div[@class='mt']/p[1]").get_attribute("innerText")
                        applicationTypes.append(applicationText)
                    except:
                        applicationTypes.append(None)
                        
                    try:
                        #get interview descriptions
                        interviewDesc = interview.find_element(By.XPATH,".//p[contains(@class,'css-w00cnv')]").get_attribute("innerText")
                        interviewDescriptions.append(interviewDesc)
                    except:
                        interviewDescriptions.append(None)
                        
                    try:
                        #get interview questions
                        #.find_element(By.CLASS_NAME,"e151mjlk2")
                        interviewQues = interview.find_element(By.XPATH,".//ul[contains(@class,'e151mjlk2')]/li[1]/span[1]").get_attribute("innerText")
                        interviewQuestions.append(interviewQues)
                    except:
                        interviewQuestions.append(None)
                totalData += 10
                totalString = str(totalData) + " Interviews Scrapped"
                print(totalString)
                #print("Done")
                #print(dateList)
                #print(titles)
                #print(results)
                #print(experiences)
                #print(difficulties)
                #print(applicationTypes)
                #print(interviewDescriptions)
                #print(interviewQuestions)
                nextBtn = driver.find_element(By.CLASS_NAME,"nextButton")
                if totalData == LIMIT:
                    keepRunning = False
                if nextBtn.is_enabled():
                    nextBtn.click()
                else:
                    keepRunning = False
            interview_data = pd.DataFrame({'Title':titles,
                                      'Date':dateList,
                                      'Result':results,
                                      'Experience':experiences,
                                      'difficulty':difficulties,
                                      'Application Type':applicationTypes,
                                      'Interview Descriptions':interviewDescriptions,
                                      'Interview Questions':interviewQuestions
                                      })
            ExcelFileName = companyname[0] + "_interviews.xlsx"
            writer = pd.ExcelWriter(ExcelFileName,engine='openpyxl')
            interview_data.to_excel(writer,sheet_name='Interviews')
            writer.save()
        except Exception as e:
            interview_data = pd.DataFrame({'Title':titles,
                                          'Date':dateList,
                                          'Result':results,
                                          'Experience':experiences,
                                          'difficulty':difficulties,
                                          'Application Type':applicationTypes,
                                          'Interview Descriptions':interviewDescriptions,
                                          'Interview Questions':interviewQuestions
                                          })
            ExcelFileName = companyname[0] + "_interviews.xlsx"
            writer = pd.ExcelWriter(ExcelFileName,engine='openpyxl')
            interview_data.to_excel(writer,sheet_name='Interviews')
            writer.save()
            print(e)
            
            
        

        

