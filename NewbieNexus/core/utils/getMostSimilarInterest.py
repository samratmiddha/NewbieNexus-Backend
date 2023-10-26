

from core.constants import INTEREST_OPTIONS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getMostSimilarInterest(input_word):

    data=INTEREST_OPTIONS
# Create a TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)

# Transform the input word into a vector
    input_vector = vectorizer.transform([input_word])

# Calculate cosine similarity between the input vector and data vectors
    similarities = cosine_similarity(input_vector, X)

# Find the most similar word
    most_similar_index = similarities.argmax()
    most_similar_word = data[most_similar_index]

    return most_similar_word