from greek_accentuation.characters import base
from nltk.corpus import stopwords

import string
import pandas as pd
from parameters import *


class Classifier:

    def __init__(self):
        # instance variable
        self.train_attributes = {'text': [], 'features': [], 'target': []}

    def train(self):
        # at this point we extract (custom) statistical features from  the training dataset
        train_set = pd.read_csv('training dataset.csv', sep=';')

        for index, row in train_set.iterrows():
            # firstly, we preprocess every training tweet
            # make tweet's text lowercase
            processed_tweet = row['Tweet'].lower()
            # remove urls, usernames and hashtags via RegularExpression
            processed_tweet = re.sub(r"(http\S+)|(@\S+)", "", processed_tweet)
            # remove punctuation
            processed_tweet = processed_tweet.translate(
                str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
            # function that removes accent from a char
            buffer_str = ''
            for char in processed_tweet:
                unaccented_character = base(char)
                buffer_str = buffer_str + unaccented_character
            processed_tweet = buffer_str
            # remove some stantard abbreviations like 'rt', 'via', 'amp'
            processed_tweet = [term for term in processed_tweet.split() if term not in stop]
            processed_tweet = ' '.join(processed_tweet)
            processed_tweet = emoji_pattern.sub(u'', processed_tweet)

            # now, we extract the features from training tweets
            # 'b' gets every position of a search query (keyword) within a tweet
            # and stores them in feat_b list
            b = next((b + 1 for b, t in enumerate(processed_tweet.split()) if t in search_queries), 0)
            c = next((c + 1 for c, t in enumerate(processed_tweet.split()) if t in places_dict.keys()), 0)
            extracted_features = {'feature_a': len(processed_tweet.split()), 'feature_b': b, 'feature_c': c}

            # we store our tweets' extracted features and their corresponding target values into lists
            self.train_attributes['features'].append(extracted_features)
            self.train_attributes['target'].append(row['Target'])
