PARAGRAPH_START = '<p>'
PARAGRAPH_END = '</p>'
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'
UNKNOWN_TOKEN = '<UNK>'
PAD_TOKEN = '<PAD>'
DOCUMENT_START = '<d>'
DOCUMENT_END = '</d>'


class VocabBuilder(object):
    def __init__(self):
        self.word_counts = {}

    def add_word(self, word):
        self.word_counts[word] = self.word_counts.get(word, 0) + 1

    def add_words(self, words):
        for word in words:
            self.add_word(word)

    def add_sent(self, sent):
        self.add_words(sent.words)

    def add_sentences(self, sentences):
        for sent in sentences:
            self.add_sent(sent)

    def _most_frequent_word_counts(self, keep_percent):
        max_size = int(keep_percent * len(self.word_counts))

        inverted_word_counts = [(count, word)
                for (word, count) in self.word_counts.items()]
        inverted_word_counts_sorted = sorted(
                inverted_word_counts, reverse=True)
        result_dict = {word: count
                for (count, word) in inverted_word_counts_sorted[:(max_size - 2)]}

        (min_count, _) = inverted_word_counts_sorted[max_size - 2]

        rest_words_count = sum([count
            for count, _ in inverted_word_counts_sorted[(max_size - 1):]])

        result_dict[PAD_TOKEN] = min_count,
        result_dict[UNKNOWN_TOKEN] = rest_words_count

        return result_dict

    def save(self, filename, keep_percent):
        most_frequent_word_counts = self._most_frequent_word_counts(keep_percent)

        with open(filename, 'w') as vocab_file:
            vocab_file.writelines(["{} {}\n".format(w, c)
                for (w, c) in most_frequent_word_counts.items()])


class Vocab(object):
  def __init__(self):
    self._word_id_counts = {}
    self._id_to_word = {}
    self._word_to_id = {}

  def add_word(self, word, count, id):
    if word in self._word_to_id:
      raise ValueError('Duplicate word {}'.format(word))

    self._word_id_counts[id] = count
    self._id_to_word[id] = word
    self._word_to_id[word] = id

  def word_id(self, word):
    if word not in self._word_to_id:
      return self._word_to_id[UNKNOWN_TOKEN]

    return self._word_to_id[word]

  def words_ids(self, words):
    return [self.word_id(word) for word in words]

  def word(self, id):
    if id not in self._id_to_word:
      raise ValueError('Id {} not found.'.format(id))

    return self._id_to_word[id]

  def words(self, ids):
    return [self.word(id) for id in ids]

  def word_count(self, word):
    return self._word_id_counts[self.word_id(word)]

  def __len__(self):
    return len(self._word_to_id)

  def check_word_id(self, word):
    if word not in self._word_to_id:
      return None
    return self._word_to_id[word]

  def sentence_start_id(self):
    return self.word_id(SENTENCE_START)

  def sentence_end_id(self):
    return self.word_id(SENTENCE_END)

  def pad_id(self):
    return self.word_id(PAD_TOKEN)



def from_file(vocab_file, max_size):
    with open(vocab_file) as f:
      vocab = Vocab()
      for ind, line in enumerate(f):
        if not line.strip():
          print('Empty line at {}'.format(ind))
          continue

        word, count = line.split()
        vocab.add_word(word, count, ind)

      assert vocab.check_word_id(UNKNOWN_TOKEN) >= 0
      assert vocab.check_word_id(PAD_TOKEN) > 0
      assert vocab.check_word_id(SENTENCE_START) > 0
      assert vocab.check_word_id(SENTENCE_END) > 0
      assert len(vocab) <= max_size

      return vocab




