import json
import os
import glob
from csv import writer

# Get Countries folder pathing
root = './data'
countrylist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
print(countrylist)

for country in countrylist:

    facebookList = []
    glassdoorList = []
    facebookFolderPathList = []
    glassdoorFolderPathList = []
    facebookDataRow = []
    glassdoorDataRow = []

    # Get All Json files and append to list
    review_root = f'./data/{country}/reviews'
    dirlist = [item for item in os.listdir(review_root) if os.path.isdir(os.path.join(review_root, item))]

    for folder in dirlist:
        # Separation of Glassdoor and Facebook based on naming of Json files
        if glob.glob(f'./data/{country}/reviews/{folder}/Glassdoor*'):
            glassdoor_name = glob.glob(f'./data/{country}/reviews/{folder}/Glassdoor*')[0]
            x = glassdoor_name.split('\\')
            glassdoorList.append(f'./data/{country}/reviews/{folder}/{x[1]}')
            glassdoorFolderPathList.append(f'{x[0]}')
        elif glob.glob(f'./data/{country}/reviews/{folder}/Facebook*'):
            facebook_name = glob.glob(f'./data/{country}/reviews/{folder}/Facebook*')[0]
            y = facebook_name.split('\\')
            facebookList.append(f'./data/{country}/reviews/{folder}/{y[1]}')
            facebookFolderPathList.append(f'{y[0]}')

    # Read data of Json files and clean it off of specials symbols or emojis
    for file in facebookList:
        print(file)
        with open(file, 'r') as json_file:
            json_object = json.load(json_file)
            for i in range(len(json_object)):
                if json_object[i]:
                    for k in range(len(json_object[i])):
                        y = json_object[i][k]['pros'].replace('\r\n', ' ').replace('\n\n', ' ') \
                            .replace('-', '').replace(',', '').replace('*', '').replace('\n', '') \
                            .replace('🤍', '').replace('😉', '').replace('🤫', '').replace('  ', '') \
                            .replace('😅', '').replace('🥀', '').replace('- - - - -', '').replace('+', '')
                        facebookDataRow.append(y)
                        c = json_object[i][k]['cons'].replace('\r\n', ' ').replace('\n\n', ' ') \
                            .replace('-', '').replace(',', '').replace('*', '').replace('\n', '') \
                            .replace('🤍', '').replace('😉', '').replace('🤫', '').replace('  ', '') \
                            .replace('😅', '').replace('🥀', '').replace('- - - - -', '').replace('+', '')
                        facebookDataRow.append(c)
                else:
                    break

    for files in glassdoorList:
        print(files)
        with open(files, 'r') as json_files:
            json_objects = json.load(json_files)
            for i in range(len(json_objects)):
                if json_objects[i]:
                    for k in range(len(json_objects[i])):
                        q = json_objects[i][k]['pros'].replace('\r\n', ' ').replace('\n\n', ' ') \
                            .replace('-', '').replace(',', '').replace('*', '').replace('\n', '') \
                            .replace('🤍', '').replace('😉', '').replace('🤫', '').replace('  ', '') \
                            .replace('😅', '').replace('🥀', '').replace('- - - - -', '').replace('+', '')
                        glassdoorDataRow.append(q)
                        b = json_objects[i][k]['cons'].replace('\r\n', ' ').replace('\n\n', ' ') \
                            .replace('-', '').replace(',', '').replace('*', '').replace('\n', '') \
                            .replace('🤍', '').replace('😉', '').replace('🤫', '').replace('  ', '') \
                            .replace('😅', '').replace('🥀', '').replace('- - - - -', '').replace('+', '')
                        glassdoorDataRow.append(b)
                else:
                    break

    if facebookList:
        with open(f'{country}_reviews_pros_cons.csv', 'a+', newline='', encoding="utf-8") as fb_write_data:
            # Create a writer object from csv module
            csv_writer = writer(fb_write_data, delimiter='\n')
            # Add contents of list as last row in the csv file
            csv_writer.writerow(facebookDataRow)
    if glassdoorList:
        with open(f'{country}_reviews_pros_cons.csv', 'a+', newline='', encoding="utf-8") as gd_write_data:
            # Create a writer object from csv module
            csv_writer = writer(gd_write_data, delimiter='\n')
            # Add contents of list as last row in the csv file
            csv_writer.writerow(glassdoorDataRow)