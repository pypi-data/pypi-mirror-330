import csv
import importlib.resources
import Levenshtein 

class LemX:
    def __init__(self, dictionary_file=None):
        if dictionary_file is None:
            #Dynamically locate dictionary.csv inside the installed package
            dictionary_file = importlib.resources.files(__package__) / "dictionary.csv"
        
        self.vocab = self.load_vocab(dictionary_file)

    def load_vocab(self, file_path):
        vocab = {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header if it exists
                for row in reader:
                    if len(row) == 2:  # Ensure valid data format
                        vocab[row[0].strip()] = row[1].strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Dictionary file not found: {file_path}")
        return vocab

    def correct_word(self, word):
        if word in self.vocab:
            return self.vocab[word]
        closest_match = min(self.vocab.keys(), key=lambda w: Levenshtein.distance(word, w))
        return self.vocab.get(closest_match, word)

    def correct_sentence(self, sentence):
        words = sentence.split()
        corrected_words = [self.correct_word(word) for word in words]
        return " ".join(corrected_words)
