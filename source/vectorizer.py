from sklearn.feature_extraction.text import CountVectorizer
import re
import pickle


# Preprocess data to remove unwanted texts like html tags and unwanted punctuation marks.
REPLACE_NO_SPACE = re.compile(
    "(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")


def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

    return reviews


reviews_train = []
for line in open('./data/movie_data/full_train.txt', 'r'):
    reviews_train.append(line.strip())
reviews_train_clean = preprocess_reviews(reviews_train)
cv = CountVectorizer(binary=True)
cv.fit(reviews_train_clean)
pickle.dump(cv.vocabulary_, open("feature.pkl", "wb"))
