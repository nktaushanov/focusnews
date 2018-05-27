import argparse
import json
import os
import re

import bs4

import example_text as et
import tokenizer
import util
import vocab


VOCAB_FILE = 'vocab.txt'


def _remove_copy_right(document):
  for p in document.find_all('p', {'class': 'inside-copy'}):
    p.clear()


def _remove_img_tags(document):
  for img in document.find_all('img'):
    img.extract()
  for top_img_div in document.find_all('div', {'class': 'inside-top-img'}):
    top_img_div.extract()


def _clear_whitespace_chars(text):
  return text.lstrip().rstrip().replace("\t", '')


def _format_html_to_text(html_text):
  doc = bs4.BeautifulSoup(html_text, 'lxml')
  _remove_copy_right(doc)
  _remove_img_tags(doc)

  return _clear_whitespace_chars(doc.text)


def _read_articles(input_dir):
  missing_articles = 0
  for input_file in os.listdir(input_dir):
    filepath = os.path.join(input_dir, input_file)
    with open(filepath, 'r') as f:
      print("Processing file {}".format(filepath))
      articles_json = json.load(f)

    for article_json in articles_json:
      if not article_json['body'] or not article_json['title']:
        missing_articles += 1
        continue

      article_body = _format_html_to_text(article_json['body'])
      article_title = _format_html_to_text(article_json['title'])

      yield article_body, article_title

  print("Total missing articles: {}".format(missing_articles))


def _article_to_example(body, title):
  return et.ExampleText(
      article=body,
      highlights=title,
      publisher='focusnews')


QUOTES = re.compile(r'["„“”]')
BUL_ABBREVIATIONS_1 = re.compile(r'(?<=[\s\d/])(хил|г|год|гр|кг|лв|лв|ст|ч|км)\.')
BUL_ABBREVIATIONS_2 = re.compile(r'(?<!\w)(обл|нар|Св|св|бр|чл|ал|нк)\.')
SLASH = re.compile(r'(?<=\s)/(?=\w)|(?<=\w)/(?=\s)')

TEXT_FILTERS = [
    lambda text: QUOTES.sub(" '' ", text),
    lambda text: BUL_ABBREVIATIONS_1.sub(r'\1 ', text),
    lambda text: BUL_ABBREVIATIONS_2.sub(r'\1 ', text),
    lambda text: SLASH.sub('/', text),
    lambda text: text.replace(' т.е.', ' т-е '),
    lambda text: text.replace(' чл.-кор.', ' чл-кор '),
    lambda text: text.replace('№', "#"),
    lambda text: text.replace(' Снимка: ', '. Снимка: '),
]


def main():
  parser = argparse.ArgumentParser(description='Converts Focus news text '
      'files to tf.Example formatted text that can be used in the '
      'textsum converter.')

  parser.add_argument('--input_dir', '-i', dest='input_dir', required=True,
      help='Input documents directory.')
  parser.add_argument('--output', '-o', dest='output', required=True,
      help='Output folder.')
  parser.add_argument('--vocab_keep', '-vk', dest='vocab_keep',
      default=1.0, type=float, help='Vocabulary keep percent.')

  args = parser.parse_args()

  words_vocab = vocab.VocabBuilder()
  articles = _read_articles(args.input_dir)
  output_file = os.path.join(args.output, "all.txt")
  with open(output_file, 'w') as f:
    for body, title in articles:
      tokenized_body = tokenizer.tokenize_text(
          body, no_punct=False, text_filters=TEXT_FILTERS)
      tokenized_title = tokenizer.tokenize_text(
          title, no_punct=False, text_filters=TEXT_FILTERS).sentences

      example_text = _article_to_example(
          tokenized_body, tokenized_title)
      f.write(example_text.to_str())

      words_vocab.add_sentences(tokenized_body.sentences)
      words_vocab.add_sentences(tokenized_title)
      words_vocab.add_words(example_text.tokens())

  words_vocab.save(os.path.join(args.output, VOCAB_FILE), args.vocab_keep)
  print('Done.')


if __name__ == '__main__':
  main()
