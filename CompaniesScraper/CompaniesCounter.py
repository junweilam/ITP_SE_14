import json

with open('D:\\CompaniesScraper\\Zimbabwe\\Zimbabwe.json', encoding='utf8') as JSONFile:
    data = json.load(JSONFile)

length = len(data)

print(length)