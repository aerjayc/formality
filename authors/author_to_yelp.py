import os.path
import pathlib
from collections import Counter
import operator
import re
from nltk import tokenize, word_tokenize

RAWDIR = 'raws/'
DATADIR = 'datasetized/'

a_fname = 'austen.txt'
b_fname = 'twain.txt'
A_ENCODING = 'utf-8'
B_ENCODING = 'latin-1'

""" Notes:
        - twain.txt uses a weird unicode character not recognized by our parser,
            so we replaced it all with double quotes '"'
        - chapter/preface/etc. indicators removed on both texts
"""



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


    pathlib.Path(DATADIR).mkdir(parents=True, exist_ok=True)    # create dir if not exist
    with open(a_text_path, 'w') as f:
        for sentence in a_parsed_sentences:
            f.write(sentence + '\n')
    with open(b_text_path, 'w') as f:
        for sentence in b_parsed_sentences:
            try:
                f.write(sentence + '\n')
            except UnicodeEncodeError:
                raise Exception(f"Weird character:\t{repr(sentence)}")

    vocab = a_vocab + b_vocab
    sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)

    with open(vocab_path, 'w') as f:
        for word,_ in sorted_vocab:
            f.write(word + '\n')



def preprocess(raw):
    """ make everything lowercase
        convert CRLF to LF
        #remove single-word paragraphs
    """
    raw = raw.lower()
    raw.replace('\r\n', '\n')

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
    paragraph.replace('\n', ' ')

    # extract sentences
    sentences = tokenize.sent_tokenize(paragraph)

    return sentences

def extract_words(sentence):
    return word_tokenize(sentence)

def parse_sentences(sentences):
    """ returns:
            parsed_sentences =  ["A dog , a cat 's tail , and a mouse .", ...]
            vocab = {word_1: freq(word_1), ...} : freq(word_i) >= freq(word_i+1)
    """
    parsed_sentences = []
    vocab = Counter()
    for sentence in sentences:
        words = extract_words(sentence)

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
    
    # sort the vocabulary by frequency
    # vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)

    return parsed_sentences, vocab

if __name__ == '__main__':
    main()