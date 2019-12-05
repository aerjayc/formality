import os.path
import pathlib
from collections import Counter
import operator
import re
from nltk import tokenize, word_tokenize

WORDLIM = 21
CHARLIM = 15

RAWDIR = 'raws/'
DATADIR = 'datasetized/'

a_fname = 'austen.txt'
b_fname = 'twain.txt'
A_ENCODING = 'utf-8'
B_ENCODING = 'latin-1'



def main():
    # paths to author corpora
    a_path = os.path.join(RAWDIR, a_fname)
    b_path = os.path.join(RAWDIR, b_fname)
    # paths to datasetized corpora
    a_text_path = os.path.join(DATADIR, a_fname + '.text')
    a_labels_path = os.path.join(DATADIR, a_fname + '.labels')
    b_text_path = os.path.join(DATADIR, b_fname + '.text')
    b_labels_path = os.path.join(DATADIR, b_fname + '.labels')
    vocab_path = os.path.join(DATADIR, 'vocab')
    text_path = os.path.join(DATADIR, 'text')
    labels_path = os.path.join(DATADIR, 'labels')


    # import corpora
    with open(a_path, 'rb') as f:
        a_raw = f.read().decode(A_ENCODING)
    with open(b_path, 'rb') as f:
        b_raw = f.read().decode(B_ENCODING)

    # preprocessing
    a_raw = preprocess(a_raw)
    b_raw = preprocess(b_raw)

    # extract paragraphs
    a_paragraphs = combine_paragraphs(a_raw)
    b_paragraphs = combine_paragraphs(b_raw)

    # extract sentences/21-word phrases
    a_sentences = extract_sentences(a_paragraphs)
    b_sentences = extract_sentences(b_paragraphs)

    # extract words
    a_parsed_sentences, a_vocab = parse_sentences(a_sentences)
    b_parsed_sentences, b_vocab = parse_sentences(b_sentences)


    # write data to files
    pathlib.Path(DATADIR).mkdir(parents=True, exist_ok=True)    # create dir if not exist
    with open(a_text_path, 'w') as f:
        for sentence in a_parsed_sentences:
            try:
                f.write(sentence + '\n')
            except UnicodeEncodeError:
                raise Exception(f"Weird character:\t{repr(sentence)}")
    with open(a_labels_path, 'w') as f:
        f.write('0\n'*len(a_parsed_sentences))

    with open(b_text_path, 'w') as f:
        for sentence in b_parsed_sentences:
            try:
                f.write(sentence + '\n')
            except UnicodeEncodeError:
                raise Exception(f"Weird character:\t{repr(sentence)}")
    with open(b_labels_path, 'w') as f:
        f.write('1\n'*len(b_parsed_sentences))

    vocab = a_vocab + b_vocab
    sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)

    with open(vocab_path, 'w') as f:
        for word,_ in sorted_vocab:
            f.write(word + '\n')


    with open(text_path, 'w') as f:
        with open(a_text_path) as fa:
            a_text = fa.read()
        with open(b_text_path) as fb:
            b_text = fb.read()
        f.write(a_text + b_text)

    with open(labels_path, 'w') as f:
        with open(a_labels_path) as fa:
            a_labels = fa.read()
        with open(b_labels_path) as fb:
            b_labels = fb.read()
        f.write(a_labels + b_labels)


def preprocess(raw):
    """ make everything lowercase
        convert CRLF to LF
        replace {';', '--'} with '.'
        remove underscores
    """
    raw = raw.lower()
    raw = raw.replace('\r\n', '\n')
    raw = raw.replace(';', '.')
    raw = raw.replace('--', '. ')
    raw = raw.replace('_', '')

    return raw

def combine_paragraphs(raw):
    """ format:
            <paragraph>\n...\n
            <paragraph>\n...\n
            ...
            <paragraph>
    """
    combined = re.sub(r"\n{2,}", ' ', raw)
    #paragraphs = re.split(r"\n{2,}", raw)
    return combined

def extract_sentences(paragraph):
    """ format:
            <sentence>. "<sentence>?"
    """
    # replace newlines with spaces (within paragraphs)
    # paragraph.replace('\n', ' ')

    # extract sentences
    sentences = tokenize.sent_tokenize(paragraph)

    return sentences

def extract_words(sentence):
    words = word_tokenize(sentence)

    split_wordsets = break_wordset(words)

    return split_wordsets

def break_wordset(words):
    """ recursively breaks down words using
        half_wordset(), which uses commas as breakpoints
    """

    if len(words) > WORDLIM:
        if ',' in words:
            w1, w2 = half_wordset(words)
            return break_wordset(w1) + break_wordset(w2)
        else:
            breakpoint = len(words) >> 1
            return [words[:breakpoint], words[breakpoint:]]
    else:
        return [words]

def half_wordset(words):
    # break at the middle (appropriate) punctuation
    # if none, break at middle
    comma_indices = [i for i,word in enumerate(words) if word==',']
    middle = len(comma_indices)/2
    
    # argmin_i(middle - i)
    breakpoint = min(comma_indices, key=lambda x:abs(x-middle))
    
    words[breakpoint] = '.'

    return [words[:breakpoint+1], words[breakpoint+1:]]

def parse_sentences(sentences):
    """ returns:
            parsed_sentences =  ["A dog , a cat 's tail , and a mouse .", ...]
            vocab = {word_1: freq(word_1), ...} : freq(word_i) >= freq(word_i+1)
    """
    parsed_sentences = []
    vocab = Counter()
    for sentence in sentences:
        wordss = extract_words(sentence)

        for words in wordss:
            parsed_sentence = ''
            for i, word in enumerate(words):
                if i == 0:
                    parsed_sentence += word
                else:
                    parsed_sentence += ' ' + word   # separate words by spaces
            
                if word in vocab:
                    vocab[word] += 1                # count word frequency
                else:
                    vocab[word] = 1
            
            #print(parsed_sentence)
            parsed_sentences.append(parsed_sentence)

    return parsed_sentences, vocab

if __name__ == '__main__':
    main()