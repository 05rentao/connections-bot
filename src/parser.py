import os
import json
import pandas as pd

dates = []
words = []
yellow_words, green_words, blue_words, purple_words = [], [], [], []
yellow_group, green_group, blue_group, purple_group = [], [], [], []

for filename in os.listdir('data/raw/'):
    with open(f'data/raw/{filename}', "r", encoding="utf-8") as f:

        puzzle = json.load(f)
        print(f"Processing file: {filename}")
        
        content = 'content'
        if filename.startswith('2024-12-12'):
            content = 'image_alt_text'
        elif filename.startswith('2025-04-01'):
            continue

        dates.append(puzzle['print_date'])
        y, g, b, p = [], [], [], []

        yellow_group.append(puzzle['categories'][0]['title'])
        for card in puzzle['categories'][0]['cards']:
            y.append(card[content])

        green_group.append(puzzle['categories'][1]['title'])
        for card in puzzle['categories'][1]['cards']:
            g.append(card[content])

        blue_group.append(puzzle['categories'][2]['title'])
        for card in puzzle['categories'][2]['cards']:
            b.append(card[content])

        purple_group.append(puzzle['categories'][3]['title'])
        for card in puzzle['categories'][3]['cards']:
            p.append(card[content])

        ygbp = y + g + b + p
        words.append(ygbp)
        yellow_words.append(y)
        green_words.append(g)
        blue_words.append(b)
        purple_words.append(p)

d = {'dates': dates,
     'words': words,
     'yellow_words': yellow_words,
     'green_words': green_words,
     "blue_words": blue_words,
     "purple_words": purple_words,
     'yellow_group': yellow_group,
     'green_group': green_group,
     'blue_group': blue_group,
     'purple_group': purple_group
     }

pd.DataFrame(d).to_csv('data/words.csv', index=True)
print("Data saved to data/words.csv")