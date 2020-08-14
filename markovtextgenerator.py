import markovchain
import itertools

text_generator = markovchain.TextGenerator(2, markovchain.Token.word)

data = "Chapter 1-3.txt"
text_generator.train_text_file(data)

# data = "https://www.cnn.com/2019/12/06/politics/elizabeth-warren-physical-exam/index.html"
# text_generator.train_url(data)

for i in itertools.islice(text_generator.generate(), 300):
    print(str(i) + " ", end="")
