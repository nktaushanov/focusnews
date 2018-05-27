import string

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import wordpunct_tokenize


def tokenize_sent(sentence, lower_case, no_punct):
  words = word_tokenize(sentence)
  if no_punct:
    words = [word for word in words
        if not all(char in string.punctuation for char in word)]

  if lower_case:
    return Sentence([word.lower() for word in words], sentence)
  else:
    return Sentence(words, sentence)


def tokenize_sentences(sentences, lower_case=True, no_punct=True):
  return Document(
      [tokenize_sent(sent, lower_case, no_punct) for sent in sentences],
      " \n".join(sentences))


def tokenize_text(document, lower_case=True, no_punct=True, text_filters=[]):
  filtered_document = document
  for filtr in text_filters:
    filtered_document = filtr(filtered_document)

  return Document(
      [tokenize_sent(sent, lower_case, no_punct)
        for sent in sent_tokenize(filtered_document)],
      document)


class Sentence(object):
  def __init__(self, words, original=None):
    self.words = words
    self.original = original

  def __repr__(self):
    return "Sentence(words={}, original=\"{}\")".format(
        self.words, self.original)

  def simple(self):
    return " ".join(self.words)


class Document(object):
  def __init__(self, sentences, original=None):
    self.sentences = sentences
    self.original = original

  def simple(self):
    return [sentence.simple() for sentence in self.sentences]

  def __repr__(self):
    return "Document(sentences={}, original=\"{}\"".format(
        self.sentences, self.original)

