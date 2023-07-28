import json
import os


json_path = 'data\\Singapore\\reviews\\ASEF\\Facebook_2-ASEF-6.json'

# Country Instrumental Total (Quantitative)
cit = 0
# Country Instrumental Counter (Quantitative)
cic = 0
# Country Experiential Total (Quantitative)
cet = 0
# Country Experiential Counter (Quantitative)
cec = 0
# Country Symbolic Total (Quantitative)
cst = 0
# Country Symbolic Counter (Quantitative)
csc = 0

# Country Experiential Total (Qualitative)
cet2 = 0
# Country Experiential Counter (Qualitative)
cec2 = 0
# Country Instrumental Total (Qualitative)
cit2 = 0
# Country Instrumental Counter (Qualitative)
cic2 = 0

# Array to store companies scores of the country (reviews)
country_scores = []

# Array to store companies scores of the country (interviews)
interview_country_scores = []

total_companies = 0
total_reviews = 0

total_interviews = 0

# Function to read the json file
def read_json_file(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)
    return data

# Function to get all file names in the folder
def get_file_names_in_folder(folder_path):
    file_names = []
    for filename in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, filename)):
            file_names.append(filename)
    return file_names

# Function to read all json files in the folder
def read_all_json_files_in_folder(folder_path):
    json_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    json_content = json.load(file)
                    json_data.append(json_content)
                except json.JSONDecodeError:
                    print(f"Error: Unable to parse JSON in file '{file_path}'.")
    return json_data

# Function to get the scores from the json file
def get_score(data, type, array):
    for entry_list in data:
        for entry in entry_list:
            for entry2 in entry:
                score = entry2.get(type,None)
                if score is not None:
                    array.append(score)

# Function to get the scores from json that are not int
def get_words_score(data, type, array):
    for entry_list in data:
        for entry in entry_list:
            for entry2 in entry:
                score = 0
                word = entry2.get(type,None)
                if word is not None:
                    if word == "Yes":
                        score = 5
                    elif word == "Neutral":
                        score = 3
                    elif word == "No":
                        score = 0
                    elif word == "Good":
                        score = 5
                    elif word == "Bad":
                        score = 0
                    elif "Negative" in word:
                        score = 0
                    elif "Neutral" in word:
                        score = 3
                    elif "Positive" in word:
                        score = 5
                    elif "Difficult" in word:
                        score = 0
                    elif "Average" in word:
                        score = 3
                    elif "Easy" in word:
                        score = 5
                    elif word == "N/A":
                        score = "N/A"
                    array.append(score)


# Function to get the average of instrumental for Quantitative (Work Life Balance, Career Opportunities, Compensation and Benefits, Senior Management)
def get_instrumental_avg(work_life,career,compensation,management):
    global cit, cic
    total_score = 0
    counter = 0
    for score in work_life:
        if isinstance(score, int):
            total_score += score
            cit = cit + score 
            counter += 1
            cic = cic + 1
    for score in career:
        if isinstance(score, int):
            total_score += score
            cit = cit + score
            counter += 1
            cic = cic + 1
    for score in compensation:
        if isinstance(score, int):
            total_score += score
            cit = cit + score
            counter += 1
            cic = cic + 1
    for score in management:
        if isinstance(score, int):
            total_score += score
            cit = cit + score
            counter += 1
            cic = cic + 1
    
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

# Function to get the average of instrumental for quatitative (Business Outlook)
def get_quatitative_instrumental_avg(business):
        total_score = 0
        counter = 0
        global cit2, cic2
        for score in business:
            if isinstance(score, int):
                total_score += score
                cit2 = cit2 + score
                counter += 1
                cic2 = cic2 + 1

        if counter != 0:
            return "{:.2g}".format(total_score/counter)
        else:
            return 0

# Function to get the average of experiential (Culture & Values)
def get_experiential_avg(culture):
    global cet, cec
    total_score = 0
    counter = 0
    for score in culture:
        if isinstance(score, int):
            total_score += score
            cet = cet + score
            counter += 1
            cec = cec + 1

    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0
    
# Function to get the average of Symbolic for interview
def get_int_symbolic_avg(difficulty):
    global cst, csc
    total_score = 0
    counter = 0
    for score in difficulty:
        if isinstance(score, int):
            total_score += score
            cst = cst + score
            counter += 1
            csc = csc + 1

    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0


# Function to get the average of experiential for qualitative
def get_qualitative_experiential_avg(recommended, ceo):
    global cet2, cec2
    total_score = 0
    counter = 0
    for score in recommended:
        if isinstance(score, int):
            total_score += score
            cet2 = cet2 + score
            counter += 1
            cec2 = cec2 + 1
    for score in ceo:
        if isinstance(score, int):
            total_score += score
            cet2 = cet2 + score
            counter += 1
            cec2 = cec2 + 1

    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

# Function to get the average of Symbolic (Culture & Values, Diversity and Inclusion)
def get_symbolic_avg(culture,diversity):
    global cst, csc
    total_score = 0
    counter = 0
    for score in culture:
        if isinstance(score, int):
            total_score += score
            cst = cst + score
            counter += 1
            csc = csc + 1
    
    for score in diversity:
        if isinstance(score, int):
            total_score += score
            cst = cst + score
            counter += 1
            csc = csc + 1

    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

wlt = 0
wlc = 0
def get_avg_wl(array):
    global wlt, wlc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            wlt = wlt + score
            wlc = wlc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

cvt = 0
cvc = 0
def get_avg_cul(array):
    global cvt, cvc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            cvt = cvt + score
            cvc = cvc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0
    
dit = 0 
dic = 0
def get_avg_div(array):
    global dit, dic
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            dit = dit + score
            dic = dic + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

caot = 0
caoc = 0
def get_avg_co(array):
    global caot, caoc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            caot = caot + score
            caoc = caoc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

cbt = 0
cbc = 0
def get_avg_com(array):
    global cbt, cbc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            cbt = cbt + score
            cbc = cbc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

smt = 0
smc = 0
def get_avg_sm(array):
    global smt, smc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            smt = smt + score
            smc = smc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0

rect = 0
recc = 0
def get_avg_rec(array):
    global rect, recc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            rect = rect + score
            recc = recc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0
            
appt = 0
appc = 0
def get_avg_app(array):
    global appt, appc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            appt = appt + score
            appc = appc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0    

bot = 0
boc = 0
def get_avg_bo(array):
    global bot, boc
    total_score = 0
    counter = 0
    for score in array:
        if isinstance(score, int):
            total_score += score
            counter += 1
            bot = bot + score
            boc = boc + 1
    if counter != 0:
        return "{:.2g}".format(total_score/counter)
    else:
        return 0  
# Function to get the company scores (interviews)
def get_int_company_scores(company_name, country):
    experience_scores = []
    difficulties_scores = []
    global total_interviews

    try:
        json_data = read_all_json_files_in_folder(f'data\\{country}\\interviews\\{company_name}')

        for data in json_data:
            for data2 in data:
                for data3 in data2:
                    total_interviews += len(data3)

        # Get Interview Experience Score
        get_words_score(json_data,"experience", experience_scores)

        # Get Interview Difficulties Score
        get_words_score(json_data,"difficulties", difficulties_scores)

        experience_score = get_experiential_avg(experience_scores)
        difficulties_score = get_int_symbolic_avg(difficulties_scores)

        print(f'Experience Average Score(Quatitative): {experience_score}')
        print(f'Difficulties Average Score(Quatitative): {difficulties_score}')

        interview_country_scores.append({
            "Company Name: " : company_name,
            "Experience Score(Quatitative): " : experience_score,
            "Difficulties Score(Quatitative): " : difficulties_score
        })

    except FileNotFoundError:
        print(f"File '{json_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Function to get the company scores (reviews)
def get_company_scores(company_name, country):
    global total_reviews
    work_life_scores = []
    culture_value_scores = []
    diversity_scores = []
    career_opp_scores = []
    compensation_scores = []
    senior_management_scores = []
    recommended_scores = []
    ceo_scores = []
    business_outlook_scores = []

    try:
        # json_data = read_json_file(json_path)
        json_data = read_all_json_files_in_folder(f'data\\{country}\\reviews\\{company_name}')

        for data in json_data:
            for data2 in data:
                for data3 in data2:
                    total_reviews += len(data3)

        
        # Get Work Life Balance Scores
        get_score(json_data,"Work/Life Balance",work_life_scores)

        # Get Culture and Values Scores
        get_score(json_data,"Culture & Values", culture_value_scores)

        # Get Diversity and Inclusion Scores
        get_score(json_data,"Diversity and Inclusion", diversity_scores)

        # Get Career Opportunities Scores
        get_score(json_data,"Career Opportunities",career_opp_scores)

        # Get Compensation and Benefits Scores
        get_score(json_data,"Compensation and Benefits",compensation_scores)

        # Get Senior Management Scores
        get_score(json_data,"Senior Management", senior_management_scores)

        # Get Recommended Scores
        get_words_score(json_data,"Recommended", recommended_scores)

        # Get CEO Approval Scores
        get_words_score(json_data,"CEO Approval", ceo_scores)

        # Get Business Outlook Scores
        get_words_score(json_data,"Business Outlook", business_outlook_scores)

        instrumental_average = get_instrumental_avg(work_life_scores,career_opp_scores,compensation_scores,senior_management_scores)
        # experiential_average = get_experiential_avg(culture_value_scores)
        # symbolic_average = get_symbolic_avg(culture_value_scores,diversity_scores)
        # quatitative_instrumental = get_quatitative_instrumental_avg(business_outlook_scores)
        # quatitative_experiential = get_qualitative_experiential_avg(recommended_scores,ceo_scores)
        work_life_balance = get_avg_wl(work_life_scores)
        culture_and_values = get_avg_cul(culture_value_scores)
        diversity = get_avg_div(diversity_scores)
        career = get_avg_co(career_opp_scores)
        compensation = get_avg_com(compensation_scores)
        senior_management = get_avg_sm(senior_management_scores)
        recommended = get_avg_rec(recommended_scores)
        approval = get_avg_app(ceo_scores)
        business_outlook = get_avg_bo(business_outlook_scores)

        print(f'Company: {company_name}')
        # print(f'Instrumental Average(Quantitative): {instrumental_average}')
        # print(f'Experiential Average(Quantitative): {experiential_average}')
        # print(f'Symbolic Average(Quantitative): {symbolic_average}')
        # print(f'Instrumental Average(Quatitative): {quatitative_instrumental}')
        # print(f'Experiential Average(Quatitative): {quatitative_experiential}')
        print(f'Work/Life Balance (Quatitative): {work_life_balance}')
        print(f'Culture & Values (Quatitative): {culture_and_values}')
        print(f'Diversity: {diversity}')
        print(f'Career: {career}')
        print(f'Compensation: {compensation}')
        print(f'Senior Management: {senior_management}')
        print(f'Recommended: {recommended}')
        print(f'CEO Approval:  {approval}')
        print(f'Business Outlook: {business_outlook}')
        print("--------------------------")

        country_scores.append({
            company_name:{
                "Company Name:": company_name,
                # "Instrumental Average(Quantitative)": instrumental_average,
                # "Experiential Average(Quantitative)": experiential_average,
                # "Symbolic Average(Quantitative)" : symbolic_average,
                # "Instrumental Average(Quatitative)" : quatitative_instrumental,
                # "Experiential Average(Quatitative)" : quatitative_experiential
                "Work/Life Balance (Quantitative): ": work_life_balance,
                "Culture & Values (Quantitative): ": culture_and_values,
                "Diversity and Inclusion (Quantitative): ": diversity,
                "Career Opportunities (Quantitative): ": career,
                "Compensation and Benefits (Quantitative): " : compensation,
                "Senior Management (Quantitative): " : senior_management,
                "Recommended (Qualitative): " : recommended,
                "CEO Approval (Qualitative): " : approval,
                "Business Outlook (Qualitative): " : business_outlook
            }

        })

    except FileNotFoundError:
        print(f"File '{json_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# ====================================================================================================================================================
# MAIN
# Country
country = "Netherlands"

# Folder path (Country)
# folder_path = f"data\\{country}\\reviews"

# For interviews
folder_path = f"data\\{country}\\interviews"

# Get all the file names and store in an array
file_names_array = get_file_names_in_folder(folder_path)

# for all the folders in the country file, get each of the company_scores
for company in file_names_array:
    # For reviews
    # get_company_scores(company,country)
    # For interviews
    get_int_company_scores(company,country)

# file path to where to store the score json
# file_path = f'data\\{country}\\reviews_scores.json'

# for interviews
file_path = f'data\\{country}\\interviews_scores.json'

# Storing the data in the json
with open(file_path,"w",encoding='utf-8') as json_file:
    # For reviews
    # json.dump(country_scores, json_file)
    # For interviews
    json.dump(interview_country_scores, json_file)


# ============================================== Reviews =======================================================
# print(f'====================================')
# print(f'{country} Total Average: ')
# print(f'Instrumental Average(Quantitative): {"{:.2g}".format(cit/cic)}')
# print(f'Experiential Average(Quantitative): {"{:.2g}".format(cet/cec)}')
# print(f'Symbolic Average(Quantitative): {"{:.2g}".format(cst/csc)}')
# print(f'Instrumental Average(Quatitative): {"{:.2g}".format(cit2/cic2)}')
# print(f'Experiential Average(Quatitative): {"{:.2g}".format(cet2/cec2)}')
# print(f'====================================')

# ============================================== Reviews =======================================================

# ============================================== Interviews =======================================================
# print(f'====================================')
# print(f'{country} Total Average: ')
# print(f'Instrumental Average(Quatitative): {"{:.2g}".format(cet/cec)}')
# print(f'Experiential Average(Quatitative): {"{:.2g}".format(cst/csc)}')
# print(f'====================================')
# ============================================== Interviews =======================================================

print(f'Average interviews for {country} : {total_interviews/len(file_names_array)}')
print(f'total reviews : {total_interviews}')
print(f'Companies: {len(file_names_array)}')

# country_file_name = "data\\country_avg_scores.json"

country_file_name = "data\\country_interviews_avg_scores.json"

if os.path.exists(country_file_name):
    with open(country_file_name, "r") as file:
        existing_data = json.load(file)
else:
    existing_data = {}

key_to_append = f'{country}'

# ============================================== Reviews =======================================================
# new_data = {country: {
#     "Work/Life Balance (Quantitative): ": "{:.2g}".format(wlt/wlc),
#     "Culture & Values (Quantitative): ": "{:.2g}".format(cvt/cvc),
#     "Diversity and Inclusion (Quantitative): ": "{:.2g}".format(dit/dic),
#     "Career Opportunities (Quantitative): ": "{:.2g}".format(caot/caoc),
#     "Compensation and Benefits (Quantitative): " : "{:.2g}".format(wlt/wlc),
#     "Senior Management (Quantitative): " : "{:.2g}".format(smt/smc),
#     "Recommended (Qualitative): " : "{:.2g}".format(rect/recc),
#     "CEO Approval (Qualitative): " : "{:.2g}".format(appt/appc),
#     "Business Outlook (Qualitative): " : "{:.2g}".format(bot/boc)
#     # "Experiential Average(Quantitative): ": "{:.2g}".format(cet/cec),
#     # "Symbolic Average(Quantitative): ": "{:.2g}".format(cst/csc),
#     # "Instrumental Average(Quatitative)": "{:.2g}".format(cit2/cic2),
#     # "Experiential Average(Quatitative)": "{:.2g}".format(cet2/cec2)
# }}
# ============================================== Reviews =======================================================

# ============================================== Interviews =======================================================
new_data = {country: {
    "Experience Score(Quatitative): ": "{:.2g}".format(cet/cec),
    "Difficulty Score(Quatitative): ": "{:.2g}".format(cst/csc)
}}

# ============================================== Interviews =======================================================

if key_to_append not in existing_data:
    existing_data[key_to_append] = new_data[key_to_append]
else:
    existing_data[key_to_append].update(new_data[key_to_append])

with open(country_file_name, "w") as file:
    json.dump(existing_data, file, indent=4)