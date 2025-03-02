# LemX

LemX is a Banglish lemmatizer and word corrector utilizing Levenshtein Distance. It was developed by Pronoy Kumar Mondal and Sadman Sadik Khan under the supervision of Md. Sadekur Rahman, in collaboration with the DIU NLP & ML Research Lab.

## Installation

LemX can be installed directly from PyPI using pip:

```bash
pip install lemx
```

## Usage

### Word Correction & Lemmatization

```python
from lemx import Lemmatizer

lemmatizer = Lemmatizer()

# Correct and lemmatize a single word
incorrect_word = "amr"
corrected_word = lemmatizer.correct(incorrect_word)

print(f"Corrected word for '{incorrect_word}': {corrected_word}")
```

### Sentence Correction & Lemmatization

```python
from lemx import LemX

lemmatizer = LemX()

sentence = "ajkei ami valo asi"
corrected_sentence = lemmatizer.correct_sentence(sentence)

print(f"Corrected sentence: {corrected_sentence}")
```

## Features

- **Banglish Word Lemmatization**: Converts inflected forms to their base forms.
- **Banglish Word Correction**: Uses Levenshtein Distance for error correction.
- **Lightweight & Easy to Use**: Simple API for seamless integration.

## Contributing

We welcome contributions! If you'd like to improve LemX, feel free to:
- Open an issue for bug reports or feature requests.
- Submit a pull request with your improvements.

