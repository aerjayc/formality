import re
from collections import Counter
import operator
import pandas as pd
import sklearn.model_selection

def list_words(text, formatted=False):
    regexp = r"([\w" + re.escape(r"#$-%*_\/")
    regexp += r"""]+)(?:([\.\!\?])(['"])?$)|(?:(['"\(\[])?(?:(?:(\w+)""" + r"(n't|'s|'ve|'m|'ll|'re|'d|'n|'em))|" + "([\w"
    regexp += re.escape(r"#$.'-%*_\/") + r"""]+))([!?,;:+-])?(['"\)\]])?)"""

    words = []
    if formatted:
        words = re.split(' ', text)
    else:
        matches = re.findall(regexp, text, re.IGNORECASE)
        for group in matches:
            for word in group:
                if word:
                    words.append(word.lower())

    return words

def yelpify_line(line, vocab, formatted=False):
    form_list = re.split('\t', line)

    text = form_list[3]
    if text[-1] == '\n':
        text = text[:-1]
    if text[-1] == '\r':
        text = text[:-1]

    words = list_words(text, formatted=formatted)

    yelped_text = ""
    for i, word in enumerate(words):
        if word.lower() in vocab:
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


    return mean, yelped_text

def formality_to_yelp(filename, formatted=False):
    path_to_formality = f'formality/{filename}'
    path_to_text = f'formality/modified/{filename}.train.text'
    path_to_labels = f'formality/modified/{filename}.train.labels'
    path_to_vocab = f'formality/modified/{filename}.train.vocab'
    path_to_combined = f'formality/modified/{filename}.train'

    vocab = Counter()

    # with open(path_to_text, 'w') as ft:
        # pass
    # with open(path_to_labels, 'w') as fl:
        # pass
    with open(path_to_vocab, 'w') as fv:
        pass
    with open(path_to_combined, 'w') as fc:
        pass

    #import formality text file
    with open(path_to_formality, 'rb') as ff:
        line  = ff.readline().decode('latin-1')
        #i = 0
        while(line):
            yelped_line = yelpify_line(line, vocab, formatted=formatted)
            print(yelped_line)

            # with open(path_to_labels, 'a') as fl:
                # fl.write(yelped_line[0])
                # fl.write('\n')
            # with open(path_to_text, 'a') as ft:
                # ft.write(yelped_line[1])

            with open(path_to_combined, 'a') as fc:
                fc.write(yelped_line[0] + '\t' + yelped_line[1] + '\n')

            line = ff.readline().decode('latin-1')

    #with open(path_to_vocab, 'w') as fv:
    #    for word, freq in vocab.items():
    #        fv.write(word + "\t" + str(freq))
    #        fv.write('\n')
    return vocab

def main():
    filenames = ['blog', 'news', 'answers', 'email']
    vocab = formality_to_yelp('blog', formatted=False)
    vocab += formality_to_yelp('news', formatted=False)
    vocab += formality_to_yelp('answers', formatted=True)
    vocab += formality_to_yelp('email', formatted=True)


    print("sorting vocab...")
    sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)
    print("done sorting vocab.")

    with open('formality/modified/all.train.vocab', 'w') as fv:
        for word,_ in sorted_vocab:
            fv.write(word + "\n")


    with open('formality/modified/all.train', 'w') as f:
        f.write("label\ttext\n")
    for filename in filenames:
        with open(f'formality/modified/{filename}.train') as f:
            part = f.read()
        with open(f'formality/modified/all.train', 'a') as f:
            f.write(part)
    with open('formality/modified/all.train', 'rb') as f:
        temp = f.read()
    with open('formality/modified/all.train', 'wb') as f:
        temp = f.write(temp.replace(b'\r\n', b'\n')

    all_train = pd.read_csv('formality/modified/all.train', sep='\t', encoding='latin-1')
    train, test = sklearn.model_selection.train_test_split(a, train_size=0.7)
    val, test = sklearn.model_selection.train_test_split(test, train_size=0.3333)

    train['label'].to_csv('formality/modified/split/train.label', header=False, index=False)
    train['text'].to_csv('formality/modified/split/train.text', header=False, index=False)
    val['label'].to_csv('formality/modified/split/val.label', header=False, index=False)
    val['text'].to_csv('formality/modified/split/val.text', header=False, index=False)
    test['label'].to_csv('formality/modified/split/test.label', header=False, index=False)
    test['text'].to_csv('formality/modified/split/test.text', header=False, index=False)

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