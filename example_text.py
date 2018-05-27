import vocab

class ExampleText(object):
  def __init__(self, article=None, highlights=None, publisher='none'):
    self.article = article
    self.highlights = highlights or []
    self.publisher = publisher

  def add_article(self, article):
    self.article = article
    return self

  def add_highlight(self, highlight):
    self.highlights.append(highlight)
    return self

  def add_highlights(self, highlights):
    self.highlights.extend(highlights)
    return self

  def tokens(self):
    sent_count = len(self.article.sentences) + len(self.highlights)
    sent_tokens = [vocab.SENTENCE_START, vocab.SENTENCE_END] * sent_count

    doc_tokens = [
        vocab.DOCUMENT_START, vocab.PARAGRAPH_START,
        vocab.PARAGRAPH_END, vocab.DOCUMENT_END] * 2

    return sent_tokens + doc_tokens

  def to_str(self):
    assert self.article is not None
    assert len(self.highlights) > 0
    assert self.publisher is not None

    article_str = _sentences_to_str(self.article.simple())
    summary_str = _sentences_to_str(
        [highlight.simple() for highlight in self.highlights])

    return "article={}\tabstract={}\tpublisher={}\n".format(
        article_str, summary_str, self.publisher)


def _escape_text(text):
  return text.replace("\"", "''").replace('=', '--')


def _sentences_to_str(sentences):
  escaped_sentences = [_escape_text(sent) for sent in sentences]
  sentences_str = ' '.join([
    vocab.SENTENCE_START + ' ' + sent + ' ' + vocab.SENTENCE_END
    for sent in escaped_sentences])
  doc_str = ' '.join([vocab.DOCUMENT_START, vocab.PARAGRAPH_START,
      sentences_str, vocab.PARAGRAPH_END, vocab.DOCUMENT_END])

  return doc_str


def remove_special_words(text):
  return text.replace(vocab.PARAGRAPH_START + ' ', '') \
      .replace(vocab.SENTENCE_START + ' ', '') \
      .replace(vocab.DOCUMENT_START + ' ', '') \
      .replace(' ' + vocab.PARAGRAPH_END, '') \
      .replace(' ' + vocab.SENTENCE_END, '') \
      .replace(' ' + vocab.DOCUMENT_END, '')


