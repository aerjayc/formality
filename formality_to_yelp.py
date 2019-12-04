import re

def form_to_yelp(line, vocab):
    form_list = re.split('\t', line)

    text = form_list[3]
    if text[-1] == '\n':
            text_no_newline = text[:-1]
    for word in re.split(' ', text_no_newline):
        vocab.add(word.lower())

    mean = form_list[0]
    if float(mean) <= 0:
        mean = '0'
    else:
        mean = '1'


    return mean, text_no_newline

def formality_to_yelp(filename):
    path_to_formality = f'formality/{filename}'
    path_to_text = f'formality/modified/{filename}.train.text'
    path_to_labels = f'formality/modified/{filename}.train.labels'
    path_to_vocab = f'formality/modified/{filename}.train.vocab'

    vocab = set()

    with open(path_to_text, 'w') as ft:
        pass
    with open(path_to_labels, 'w') as fl:
        pass
    with open(path_to_vocab, 'w') as fv:
        pass

    #import formality text file
    with open(path_to_formality, 'rb') as ff:
        line  = ff.readline().decode('latin-1')
        i = 0
        while(line):
            yelped_line = form_to_yelp(line, vocab)

            if not (i % 1000):
                print(line)
            i += 1

            with open(path_to_labels, 'a') as fl:
                fl.write(yelped_line[0])
                fl.write('\n')
            with open(path_to_text, 'a') as ft:
                ft.write(yelped_line[1])

            line = ff.readline().decode('latin-1')

    with open(path_to_vocab, 'w') as fv:
        for word in vocab:
            fv.write(word)
            fv.write('\n')

def main():
    filenames = ['answers', 'blog', 'email', 'news']
    formality_to_yelp('answers')
    formality_to_yelp('blog')
    formality_to_yelp('email')
    formality_to_yelp('news')

    with open('formality/modified/all.train.text', 'w') as fall:
        pass
    with open('formality/modified/all.train.labels', 'w') as fall:
        pass

    for filename in filenames:
        with open(f'formality/modified/{filename}.train.text') as f:
            part = f.read()
        with open('formality/modified/all.train.text', 'a') as fall:
            fall.write(part)

        with open(f'formality/modified/{filename}.train.labels') as f:
            part = f.read()
        with open('formality/modified/all.train.labels', 'a') as fall:
            fall.write(part)

    with open(f'formality/modified/answers.train.vocab') as f:
        vocab = set(f.readlines())
    with open(f'formality/modified/blog.train.vocab') as f:
        vocab = vocab | set(f.readlines())
    with open(f'formality/modified/email.train.vocab') as f:
        vocab = vocab | set(f.readlines())
    with open(f'formality/modified/news.train.vocab') as f:
        vocab = vocab | set(f.readlines())

    with open('formality/modified/all.train.vocab', 'w') as fv:
        for word in vocab:
            fv.write(word)


if __name__ == '__main__':
    main()