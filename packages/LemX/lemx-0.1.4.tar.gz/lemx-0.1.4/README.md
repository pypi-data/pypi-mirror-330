# LemX

LemX is a Banglish lemmatizer and word corrector using Levenshtein Distance. It was developed by Pronoy Kumar Mondal and Sadman Sadik Khan under the supervision of Md. Sadekur Rahman, in collaboration with the DIU NLP & ML Research Lab.

## Installation

You can install LemX from PyPI using pip:

pip install lemx

## Usage
from lemx import Lemmatizer

lemmatizer = Lemmatizer()

# Lemmatization
word = "korsilam"
lemma = lemmatizer.lemmatize(word)
print(f"Lemma of '{word}': {lemma}")

# Word correction
incorrect_word = "amr"
corrected_word = lemmatizer.correct(incorrect_word)
print(f"Corrected word for '{incorrect_word}': {corrected_word}")

## Features
Banglish word lemmatization
Banglish word correction using Levenshtein Distance
Lightweight and easy to use

## Contributing
We welcome contributions! If you’d like to improve LemX, feel free to submit a pull request or open an issue.

