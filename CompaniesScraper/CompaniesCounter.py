import json

with open('D:\\CompaniesScraper\\Bangladesh\\Bangladesh.json', encoding='utf8') as JSONFile:
    data = json.load(JSONFile)

length = len(data)

print(length)