from textblob import TextBlob

def getSentiment(text):
    blob = TextBlob(text)
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                        #  ('threat', 'NN'), ('of', 'IN'), ...]

    blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])
    pol = []
    for sentence in blob.sentences:
        pol.append(sentence.sentiment.polarity)
    return pol
