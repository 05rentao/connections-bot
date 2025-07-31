import pandas as pd
import random

df = pd.read_json('data/words.json', encoding='utf-8')

rows = []

for _, row in df.iterrows():

    existing_groups = set()

    for color in ['yellow_words', 'green_words', 'blue_words', 'purple_words']:
        true_group = row[color]
        rows.append(true_group + [1])
        existing_groups.add(tuple(sorted(true_group)))
        print(true_group + [1])


    for _ in range(4):
        false_group = random.sample(row['words'], 4)
        if tuple(sorted(false_group)) not in existing_groups:
            existing_groups.add(tuple(sorted(false_group)))
            rows.append(false_group + [0])
            print(false_group + [0])


groups_df = pd.DataFrame(rows, columns=["word1", "word2", "word3", "word4", "label"])

