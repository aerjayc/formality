import re
from collections import Counter
import operator
#import pandas as pd
#import sklearn.model_selection

RAW_DIR = 'formality/'
DIRECTORY = 'formality/modified_21words/'
WORDLIMIT = 21
WORDLENLIMIT = 15

def list_words(text, formatted=False):
    # text -> [ ('word1', '', ...),
    #           ('', 'word2', '', ...),
    #            ... ]
    regexp = r"([\w" + re.escape(r"#$-%*_\/")
    regexp += r"""]+)(?:([\.\!\?])(['"])?$)|(?:(['"\(\[])?(?:(?:(\w+)""" + r"(n't|'s|'ve|'m|'ll|'re|'d|'n|'em))|" + "([\w"
    regexp += re.escape(r"#$.'-%*_\/") + r"""]+))([!?,;:+-])?(['"\)\]])?)"""

    # words = ['word1', 'word2', ...]
    words = []
    if formatted:
        words = re.split(' ', text)
    else:
        matches = re.findall(regexp, text, re.IGNORECASE)
        for group in matches:
            for word in group:
                if word:
                    words.append(word.lower())

    if len(words) > WORDLIMIT:
        return None
    for word in words:
        if len(word) > WORDLENLIMIT:
            return None

    return words

def yelpify_line(line, vocab, formatted=False):
    form_list = re.split('\t', line)

    text = form_list[3]
    if text[-1] == '\n':
        text = text[:-1]
    if text[-1] == '\r':
        text = text[:-1]

    words = list_words(text, formatted=formatted)
    if words == None:
        return None

    yelped_text = ""
    for i, word in enumerate(words):
        word = word.lower()
        if word in vocab:
            vocab[word] += 1
        else:
            vocab[word] = 1

        if i == 0:
            yelped_text += word
        else:
            yelped_text += " " + word

    mean = form_list[0]
    if float(mean) <= 0:
        mean = '0'
    else:
        mean = '1'


    return yelped_text, mean

def formality_to_yelp(filename, formatted=False):
    path_to_formality = RAW_DIR + filename
    path_to_text = DIRECTORY + filename + '.train.text'
    path_to_labels = DIRECTORY + filename + '.train.labels'
    path_to_vocab = DIRECTORY + filename + '.train.vocab'
    path_to_combined = DIRECTORY + filename + '.train'

    vocab = Counter()

    with open(path_to_text, 'w') as ft:
        pass
    with open(path_to_labels, 'w') as fl:
        pass
    # with open(path_to_vocab, 'w') as fv:
        # pass
    # with open(path_to_combined, 'w') as fc:
        # pass

    #import formality text file
    # with open(path_to_formality, 'rb') as ff:
        # line  = ff.readline().decode('latin-1')
        # i = 0
        # while(line):
            # yelped_line = yelpify_line(line, vocab, formatted=formatted)
            # print(yelped_line)

            # with open(path_to_labels, 'a') as fl:
                # fl.write(yelped_line[0])
                # fl.write('\n')
            # with open(path_to_text, 'a') as ft:
                # ft.write(yelped_line[1])
                # ft.write('\n')

#            with open(path_to_combined, 'a') as fc:
#                fc.write(yelped_line[0] + '\t' + yelped_line[1] + '\n')

    to_write_text = ""
    with open(path_to_formality, 'rb') as ff:
        lines = ff.read().decode('latin-1')
        lines = re.split('\n', lines)
        lines = lines[:-1]  # removes final '\n'

        to_write_label = ''
        to_write_text = ''
        for line in lines:
            print(line)
            yelped_line = yelpify_line(line, vocab, formatted=formatted)
            if yelped_line == None:
                continue

            yelped_text, yelped_label = yelped_line
            print(yelped_label + ' ' + yelped_text)

            to_write_text += yelped_text + '\n'
            to_write_label += yelped_label + '\n'

    with open(path_to_labels, 'w') as fl:
        fl.write(to_write_label)
    with open(path_to_text, 'a') as ft:
        ft.write(to_write_text)

    #with open(path_to_vocab, 'w') as fv:
    #    for word, freq in vocab.items():
    #        fv.write(word + "\t" + str(freq))
    #        fv.write('\n')
    return vocab

def main():
    print('starting')
    filenames = ['blog', 'news', 'answers', 'email']
    vocab = formality_to_yelp('blog', formatted=False)
    vocab += formality_to_yelp('news', formatted=False)
    vocab += formality_to_yelp('answers', formatted=True)
    vocab += formality_to_yelp('email', formatted=True)


    print("sorting vocab...")
    sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)
    print("done sorting vocab.")

    with open(DIRECTORY + 'all.train.vocab', 'w') as fv:
        for word,_ in sorted_vocab:
            fv.write(word + "\n")


    # with open('formality/modified/all.train', 'w') as f:
        # f.write("label\ttext\n")
    with open(DIRECTORY + 'all.train.text', 'w') as f:
        pass
    with open(DIRECTORY + 'all.train.labels', 'w') as f:
        pass
    for filename in filenames:
        print('doing ' + filename)
        with open(DIRECTORY + filename + '.train.text') as f:
            part = f.read()
        with open(DIRECTORY + 'all.train.text', 'a') as f:
            f.write(part)

        with open(DIRECTORY + filename + '.train.labels') as f:
            part = f.read()
        with open(DIRECTORY + 'all.train.labels', 'a') as f:
            f.write(part)

    # with open('formality/modified/all.train', 'rb') as f:
        # temp = f.read()
    # with open('formality/modified/all.train', 'wb') as f:
        # temp = f.write(temp.replace(b'\r\n', b'\n')

    # all_train = pd.read_csv('formality/modified/all.train', sep='\t', encoding='latin-1')
    # train, test = sklearn.model_selection.train_test_split(a, train_size=0.7)
    # val, test = sklearn.model_selection.train_test_split(test, train_size=0.3333)

    # train['label'].to_csv('formality/modified/split/train.label', header=False, index=False)
    # train['text'].to_csv('formality/modified/split/train.text', header=False, index=False)
    # val['label'].to_csv('formality/modified/split/val.label', header=False, index=False)
    # val['text'].to_csv('formality/modified/split/val.text', header=False, index=False)
    # test['label'].to_csv('formality/modified/split/test.label', header=False, index=False)
    # test['text'].to_csv('formality/modified/split/test.text', header=False, index=False)

    # with open('formality/modified/all.train.text', 'w') as fall:
        # pass
    # with open('formality/modified/all.train.labels', 'w') as fall:
        # pass

    # for filename in filenames:
        # with open(f'formality/modified/{filename}.train.text') as f:
            # part = f.read()
        # with open('formality/modified/all.train.text', 'a') as fall:
            # fall.write(part)

        # with open(f'formality/modified/{filename}.train.labels') as f:
            # part = f.read()
        # with open('formality/modified/all.train.labels', 'a') as fall:
            # fall.write(part)

    # with open(f'formality/modified/answers.train.vocab') as f:
        # vocab = set(f.readlines())
    # with open(f'formality/modified/blog.train.vocab') as f:
        # vocab = vocab | set(f.readlines())
    # with open(f'formality/modified/email.train.vocab') as f:
        # vocab = vocab | set(f.readlines())
    # with open(f'formality/modified/news.train.vocab') as f:
        # vocab = vocab | set(f.readlines())

    # with open('formality/modified/all.train.vocab', 'w') as fv:
        # for word in vocab:
            # fv.write(word)


if __name__ == '__main__':
    main()