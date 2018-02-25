import pandas as pd
import re
from core.stop_word_builder import StopWordBuilder


class TweetReader:
    def __init__(self, tweet_file, text_column='tweet', separator=',', encoding='latin1'):
        self.tweets_df = pd.read_csv(tweet_file, sep=separator, encoding=encoding)
        all_tweets = self.tweets_df[text_column]

        self.corpus = []
        for tweet in all_tweets:
            self.corpus.append(tweet)

    @staticmethod
    def _clean_text_data(text_array, stop_words):
        stop_builder = StopWordBuilder(stop_words)

        stop_list = stop_builder.get_stop_words()

        texts = [[word for word in re.findall('[a-z]{3,15}', str(document).lower()) if word not in stop_list] for document in text_array]

        return texts

    def get_corpus(self):
        return self.corpus

    def get_tweets_df(self):
        return self.tweets_df

    def get_total_tweets(self):
        return len(self.get_corpus())

    def extract_words_frequency(self, num_words=None, stop_word_file='', ordered='desc'):
        my_clean_tweets = []

        if len(stop_word_file) > 0:
            my_clean_tweets = TweetReader._clean_text_data(self.corpus, stop_word_file)

        freq = {}

        for tweet in my_clean_tweets:
            for word in tweet:
                count = freq.get(word, 0)
                freq[word] = count + 1

        frequency_list = freq.keys()
        results = []
        for word in frequency_list:
            tuple = (word, freq[word])
            results.append(tuple)

        byFreq = sorted(results, key=lambda word: word[1], reverse=True)

        if num_words is not None:
            byFreq = byFreq[: num_words]

        if ordered == 'asc':
            byFreq = sorted(byFreq, key=lambda word: word[1], reverse=False)

        return byFreq