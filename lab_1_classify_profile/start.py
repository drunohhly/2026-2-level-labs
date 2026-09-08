"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words

def main() -> None:
    """
    Launches an implementation.
    """
    with open("lab_1_classify_profile/assets/texts/de.txt", "r", encoding="utf-8") as file:
        de_text = file.read()
    with open("lab_1_classify_profile/assets/texts/unknown.txt", "r", encoding="utf-8") as file:
        unknown_text = file.read()
    with open("lab_1_classify_profile/assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    with open("lab_1_classify_profile/assets/texts/en.txt", "r", encoding="utf-8") as file:
        en_text = file.read()
    tokenized_text = tokenize(de_text)
    text_without_stopwords = remove_stop_words(tokenized_text, stopwords)
    calculated_frequencies = calculate_frequencies(text_without_stopwords)
    gotten_stop_words = get_top_n_words(calculated_frequencies, 7)
    return gotten_stop_words

result = main()
print(result)

if __name__ == "__main__":
    main()

