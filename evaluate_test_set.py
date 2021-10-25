import csv
import json
from main import best_match

with open('lookup.json', 'r') as file:
    data = json.load(file)

testset = []
with open('testset.csv', 'r') as file:

    w = csv.reader(file, delimiter='\t')

    for row in w:
        testset.append(row)

REMOVE_SPACES = False

output = [['target', 'query', 'token sort prediction', 'token set prediction']]
for row in testset:
    query = row[1]

    sort_matches = best_match(query, data, 'sort', remove_spaces=REMOVE_SPACES)
    set_matches = best_match(query, data, 'set', remove_spaces=REMOVE_SPACES)

    output.append([row[0], row[1], sort_matches, set_matches])

with open('testset_predictions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)


