"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import create_language_profile
from main import check_profile
from main import detect_language_by_top_n
from main import calculate_mse
from main import compare_profiles_by_mse
from main import detect_language_by_mse

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
    result = None
    tokenized_text = tokenize(de_text)
    text_without_stopwords = remove_stop_words(tokenized_text, stopwords)
    calculated_frequencies = calculate_frequencies(text_without_stopwords)
    result = get_top_n_words(calculated_frequencies, 7)
    unk_profile = create_language_profile("unknown", unknown_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    checked_unk_profile = check_profile(unk_profile)
    checked_de_profile = check_profile(de_profile)
    checked_en_profile = check_profile(en_profile)
    if checked_unk_profile == False or checked_de_profile == False or checked_en_profile == False:
        result_2 = None
    else:
        result_2 = detect_language_by_top_n(unk_profile, en_profile, de_profile, 15)
        result_3 = detect_language_by_mse(unk_profile, en_profile, de_profile)
    assert result, "Detection result is None"
    return result, result_2, result_3


result = main()
print(result)

if __name__ == "__main__":
    main()

