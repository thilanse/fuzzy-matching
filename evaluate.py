from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import json
from string import ascii_letters
import random
from main import best_match


with open('lookup.json', 'r') as file:
    data = json.load(file)

# items = [items[0] for label, items in data.items()]


def change_query(query):
    inds = [i for i, _ in enumerate(query) if not query.isspace()]
    sam = random.sample(inds, 1)
    lst = list(query)
    for ind in sam:
        lst[ind] = random.choice(ascii_letters)

    return "".join(lst).lower()

# print(change_query("apple iphone"))

REMOVE_SPACES = True

output = [['Label', 'True Value', 'Query', 'Token Sort', 'Token Set']]
for label, items in data.items():

    changed_item = items[0]
    changed_item = change_query(changed_item)
    query = f"do you have {changed_item}, i need it"

    sort_matches = best_match(query, data, 'sort', remove_spaces=REMOVE_SPACES)
    set_matches = best_match(query, data, 'set', remove_spaces=REMOVE_SPACES)
    # matches = [row['value'] for row in matches]
    output.append([label, items[0], query, sort_matches, set_matches])

with open('output.csv', 'w', newline='') as file:
    w = csv.writer(file)
    w.writerows(output)
