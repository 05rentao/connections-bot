import random
import os
import json
import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from dotenv import load_dotenv

load_dotenv()


def load_vectors():
    print('load vectors...')
    glove_path = os.getenv("GLOVE_PATH")
    return KeyedVectors.load_word2vec_format(glove_path, binary=False, no_header=True)


def get_word_samples(word_vectors):
    """
    reads from data/words.json and formats data in format closer to training data
    """
    print('get word samples...')

    df = pd.read_json('data/words.json', encoding='utf-8')

    rows = []

    for _, row in df.iterrows():

        existing_groups = set()

        for color in ['yellow_words', 'green_words', 'blue_words', 'purple_words']:
            true_group = row[color]
            rows.append(true_group + [1])
            existing_groups.add(tuple(sorted(true_group)))
            # print(true_group + [1])


        for _ in range(4):
            false_group = random.sample(row['words'], 4)
            if tuple(sorted(false_group)) not in existing_groups:
                existing_groups.add(tuple(sorted(false_group)))
                rows.append(false_group + [0])
                # print(false_group + [0])


    groups_df = pd.DataFrame(rows, columns=["word1", "word2", "word3", "word4", "label"])

    d = {'word1': list(groups_df.get('word1')),
        'word2': list(groups_df.get('word2')),
        'word3': list(groups_df.get('word3')),
        'word4': list(groups_df.get('word4')),
        'label': list(groups_df.get('label'))}

    with open('data/word_samples.json', 'w', encoding='utf-8') as f:
        json.dump(d, f)

    return groups_df

def vectorize_words(df, embedding):
    """
    takes df of word examples and converts into vectors suitable for training, returns a matrix
    """
    print('vectorize words...')
    print(f'df shape: {df.shape}')

    X = []
    y = []
    for i, row in df.iterrows():
        print(f'row: {i}')

        row_vector = []
        for key in ["word1", "word2", "word3", "word4"]:
            if row[key] not in embedding:
                embedding[row[key]] = np.zeros(embedding.vector_size)
            vector = embedding[row[key]]
            row_vector.extend(vector)
        X.append(row_vector)
        y.append(row['label'])
        
    X = np.array(X)
    y = np.array(y)

    return X, y

word_vectors = load_vectors()
df = get_word_samples(word_vectors)
X, y = vectorize_words(df, word_vectors)

np.save('all_features.npy', X)
np.save('all_labels.npy', y)