from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import json
from string import ascii_letters
import random

with open('lookup.json', 'r') as file:
    data = json.load(file)


def get_best_fuzzy_match(query, items, type, remove_spaces):
    fuzzy_output = []
    for item in items:
        item_value = item.replace(' ', '') if remove_spaces else item
        ratio = 0
        if type == 'sort':
            ratio = fuzz.token_sort_ratio(query, item_value)
        if type == 'set':
            ratio = fuzz.token_set_ratio(query, item_value)
        fuzzy_output.append({'value': item, 'ratio': ratio})

    sorted_fuzzy_output = sorted(fuzzy_output, key=lambda x: x['ratio'], reverse=True)
    # print(sorted_fuzzy_output)

    return sorted_fuzzy_output[0]


def extract_best_match(query, matches):
    choices = [match['value'] for match in matches if match['ratio'] == matches[0]['ratio']]
    print(choices)
    exact_matches = [choice for choice in choices if choice in query]
    print(exact_matches)
    best_match_value = None
    if len(exact_matches) > 0:
        best_match_value = max(exact_matches, key=len)
    else:
        best_match_value = process.extract(query, choices)[0][0]

    best_matches = [match for match in matches if match['value'] == best_match_value]

    # assert len(best_matches) == 1, "There are multiple matches with the same value. ie, duplicates"

    print(best_matches[0]['label'])
    return best_matches[0]['label']


def best_match(query, data, type, remove_spaces=False):
    query = query.replace(' ', '') if remove_spaces else query
    print(query)
    print("TOKEN SET RATIO =================")
    ratios = []
    for label, items in data.items():
        match = get_best_fuzzy_match(query, items, type, remove_spaces)
        match['label'] = label
        ratios.append(match)

    ratios = sorted(ratios, key=lambda x: x['ratio'], reverse=True)

    for row in ratios[:5]:
        print(row)

    best_match = extract_best_match(query, ratios)

    return best_match


query = "multi socket 2 usb ports"
REMOVE_SPACES = False
print("Token Sort:", best_match(query, data, 'sort', remove_spaces=REMOVE_SPACES))
print("Token Set:", best_match(query, data, 'set', remove_spaces=REMOVE_SPACES))

# choices = ['tv accessories', 'tv']
# print(process.extract(query, choices))

# First get matches from basic gazetteer, then keyword gazetteer.
# Allow entity selection for fuzzy. ei, allow only item.name to be fuzzy matched

# Take token sort match

# Take token set match

# Check if token sort match matches exactly with the string

# Check if token set match exactly with string

# Select the matching one, if both matches take the one with the longest length

# If no exact matches, select the one with the highest ratio

# If highest match is tied with more matches, find a way to filter out the correct one
