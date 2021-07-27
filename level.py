# to convert character stream into python object
import pickle

# reading from Wikipedia pickle file contains character stream
with open('word_db/enWikipediaDictTermCounts.pickle', 'rb') as file:
    # load pickle file
    d = pickle.load(file)


def get_level(word):
    # params: a word (string)
    # return: difficulty level of the english word (string)

    # {1: 'Beginner', 2: 'Basic', 3: 'Intermediate', 4: 'Expert'}

    k = d.get(word, 0)

    if 0 < k <= 500:
        return 4, k
    elif 500 < k <= 10000:
        return 3, k
    elif 10000 < k <= 30000:
        return 2, k
    elif k > 30000:
        return 1, k
    else:
        return -1, 0

# Test Drive Code

# print(get_level("tremble"))