import pandas as pd
import sklearn.model_selection

with open('formality/modified/all.train', 'rb') as f:
    temp = f.read()

temp.replace(b'\r\n', b'\n')
temp.replace(b'\n', b'\n\0')

with open('formality/modified/all.train', 'wb') as f:
    temp = f.write(temp)

all_train = pd.read_csv('formality/modified/all.train', sep='\t', encoding='latin-1')
train, test = sklearn.model_selection.train_test_split(all_train, train_size=0.7)
val, test = sklearn.model_selection.train_test_split(test, train_size=0.3333)

train['label'].to_csv('formality/modified/split/train.label', header=False, index=False)
train['text'].to_csv('formality/modified/split/train.text', header=False, index=False)
val['label'].to_csv('formality/modified/split/val.label', header=False, index=False)
val['text'].to_csv('formality/modified/split/val.text', header=False, index=False)
test['label'].to_csv('formality/modified/split/test.label', header=False, index=True)
test['text'].to_csv('formality/modified/split/test.text', header=False, index=True)