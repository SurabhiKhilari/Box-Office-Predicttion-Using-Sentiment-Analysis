# reading custom youtube comments csv
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
# import sklearn
import pickle
from dateutil.parser import parse
from datetime import datetime
import time
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import matplotlib.pyplot as plt


# Preprocess data to remove unwanted texts like html tags and unwanted punctuation marks.
REPLACE_NO_SPACE = re.compile(
    "(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")


def preprocess_reviews(yt_comment):
    yt_comment = [REPLACE_NO_SPACE.sub("", line.lower())
                  for line in yt_comment]
    yt_comment = [REPLACE_WITH_SPACE.sub(" ", line) for line in yt_comment]
    return yt_comment


def process_comments():
    comments_df = pd.read_csv("comments.csv")
    col_list = ['text', 'publishedAt', 'likes']
    comments_df = comments_df[col_list]
    # print(comments_df.nlargest(50, 'likes'))
    likes_df = comments_df.nlargest(5, 'likes')
    likes_df = likes_df[['text', 'likes']]
    yt_data = []

    for index, row in comments_df.iterrows():
        line = str(row['text'])
        # print(line)
        yt_data.append(line)
    # print(yt_data)
    yt_data_clean = preprocess_reviews(yt_data)
    # print("----------------")
    # print(yt_data_clean)
    return [yt_data_clean, likes_df]


def predict():
    # load saved vectorizer and vocabulary
    cv = CountVectorizer(
        binary=True, vocabulary=pickle.load(open("feature.pkl", "rb")))
    # Process latest comments
    yt_data = process_comments()
    X_test = cv.transform(yt_data[0])

    # Load saved prediction model
    filename = 'finalized_model.sav'
    lr = pickle.load(open(filename, 'rb'))
    array_pred = lr.predict(X_test)

    # Count neg and pos sentiment amongst retrieved youtube comments
    # Sentiment value 0 indicates negative sentiment and 1 indicates positive sentiment
    unique, counts = np.unique(array_pred, return_counts=True)
    sent_count = dict(zip(unique, counts))
    prediction = movie_prediction(sent_count)  # Stores Movie prediction
    array_neg = np.where(array_pred == 0, 1, 0)  # Stores neg sentiments

    # Prepare data for line and bar charts having monthwise count of pos and neg sentiments
    sentiment_df = pd.read_csv("comments.csv")
    col_list = ['publishedAt']
    sentiment_df = sentiment_df[col_list]
    comb_array = np.column_stack((sentiment_df.values, array_pred, array_neg))
    # print(comb_array)
    # format the date string
    for pred in comb_array:
        sent_date = re.sub('b|\'', '', pred[0])
        sent_date = datetime.strptime(
            sent_date.partition('T')[0], '%Y-%m-%d').date()
        pred[0] = sent_date
    # Count negative and positive sentiments monthwise
    comb_array = count_sentiments(comb_array)
    wordcloud_image = create_wordcloud(yt_data[0])
    # print(yt_data[1])
    return [prediction, comb_array, wordcloud_image, yt_data[1]]


def count_sentiments(sentiments):
    df = pd.DataFrame(sentiments, columns=[
        "comment_date", "sentiment", "neg_sentiment"])
    df['comment_date'] = pd.to_datetime(df['comment_date'])

    df = df.groupby(df['comment_date'].dt.strftime('%Y-%m'))[
        'sentiment', 'neg_sentiment'].sum().sort_values(by="comment_date").reset_index()
    return df


def create_wordcloud(yt_comments):
    # Prepare Data for wordcloud
    current_time = time.time()
    image_path = 'static/wordcloud_images/wordcloud'+str(current_time)+'.png'
    comment_words = ""
    for words in yt_comments:
        comment_words = comment_words + words + ' '

    # adding movie script specific stopwords
    stopwords = set(STOPWORDS)
    stopwords.add("movie")
    stopwords.add("film")
    stopwords.add("trailer")

    wordcloud = WordCloud(width=400, height=400,
                          background_color='cyan',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.tight_layout(pad=0)
    plt.savefig(image_path)
    return image_path


def movie_prediction(sent_count):
    sent_ratio = (sent_count[1]/(sent_count[0]+sent_count[1]))
    if(sent_ratio >= 0.75):
        return 1  # Superhit
    elif(sent_ratio >= 0.5):
        return 3  # Semi-hit
    else:
        return 2  # Flop


# predict()
