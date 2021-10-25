import csv
import json

data = []
with open('keyword.csv', 'r', encoding="utf-8") as file:
    csv_file = csv.reader(file)
    for row in csv_file:
        row = [i for i in row if i != '']
        data.append(row)

lookup = {}
for row in data:
    key = row[0]
    lookup[key] = []
    lookup[key].extend(row[1:])

for key, value in lookup.items():
    print(key, value)

with open('lookup.json', 'w', encoding='utf-8') as file:
    json.dump(lookup, file)