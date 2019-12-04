import re

def form_to_yelp(line, vocab):
	form_list = re.split('\t', line)
	
	text = form_list[3]
	if text[-1] == '\n':
			text = text[:-1]
	for word in re.split(' ', text):
		vocab.add(word)

	mean = form_list[0]
	if float(mean) <= 0:
		mean = '0'
	else:
		mean = '1'

	
	return mean, text

def main():
	file = 'answers'
	path_to_formality = f'formality/{file}'
	path_to_text = f'formality/modified/{file}.train.text'
	path_to_labels = f'formality/modified/{file}.train.labels'
	path_to_vocab = f'formality/modified/{file}.train.vocab'

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
		while(line):
			yelped_line = form_to_yelp(line, vocab)
			print(line)

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

if __name__ == '__main__':
	main()