import graph
import random
import itertools
import pickle
import enum
from urllib.request import urlopen

class Token(enum.Enum):
    none = 0
    character = 1
    word = 2
    byte = 3

def windowed(iterable, size):
    window = list()
    for w in iterable:
        if len(window) < size:
            window.append(w)
        else:
            window.pop(0)
            window.append(w)
        if len(window) == size:
            yield tuple(window)

class TextGenerator(object):

    # this constructor allows us to determine the level and type of tokenization the Markov Chain
    # should have
    def __init__(self, level, token=None):
        self.nodes = []
        self.level = level
        if token is None:
            self.tokenization = Token.none
        else:
            self.tokenization = token

    def generate(self):
        state = random.choice(self.nodes)
        while True:
            while state.total_weight() == 0:
                state = random.choice(self.nodes)
            rand = random.randint(0, state.total_weight() - 1)
            token = None
            for edge in state.edges:
                if rand < edge.weight:
                    token = edge.val
                    state = edge.destination
                    break
                rand -= edge.weight
            yield token

    def generate_textfile(self, filename, amount):
        if self.tokenization == Token.byte:
            with open(filename, "wb") as file:
                for i in itertools.islice(self.generate(), amount):
                    file.write(bytes([i]))
                return
        with open(filename, "w") as file:
            if self.tokenization == Token.character:
                for i in itertools.islice(self.generate(), amount):
                    file.write(str(i))
            elif self.tokenization == Token.none or self.tokenization == Token.word:
                for i in itertools.islice(self.generate(), amount):
                    file.write(str(i) + ' ')
            else:
                raise TypeError("Tokenization must be set to a valid value")

    # pickle used for serialization
    def save_pickle(self, filename):
        if isinstance(filename, str):
            file = open(filename, "wb")
        else:
            file = filename
        pickle.dump(self, file)
        file.close()

    @classmethod
    def load_pickle(cls, filename):
        if isinstance(filename, str):
            file = open(filename, "rb")
        else:
            file = filename
        rw = pickle.load(file)
        file.close()
        return rw

    def train_text_file(self, text_file):
        with open(text_file, "r", encoding="ISO-8859-1") as file:
            data = file.read().replace('\n', '')
        self.train_iterable(data)

    def train_url(self, url):
        if self.tokenization is None:
            raise TypeError("Token cannot be none")
        with urlopen(url) as request:
            if self.tokenization != Token.byte:
                data = str(request.read(), encoding="utf-8")
            else:
                data = request.read()
            self.train_iterable(data)

    def train_iterable(self, data):
        if self.tokenization == Token.word:
            processed_data = data.split()
        elif self.tokenization == Token.none or self.tokenization == Token.character or self.tokenization == Token.byte:
            processed_data = data
        previous = None
        for window in windowed(processed_data, self.level):
            token = window[-1]
            node = None
            for n in self.nodes:
                if n.val == window:
                    node = n
                    break
            if node is None:
                node = graph.Node(window)
            self.nodes.append(node)
            if previous is not None:
                previous.add_edge(token, node)
            previous = node
        