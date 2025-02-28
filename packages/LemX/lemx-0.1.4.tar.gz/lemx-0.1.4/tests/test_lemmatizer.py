
from lemx import LemX

lemmatizer = LemX("dictionary.csv")
sentence = "ajkei ami valo asi"
corrected_sentence = lemmatizer.correct_sentence(sentence)
print(corrected_sentence)  # "ajke ami bhalo achi"
