"""
Language detection starter.
"""

# pylint: disable=unused-variable, duplicate-code
from main import (
                calculate_frequencies,
                check_profile,
                collect_profiles,
                create_language_profile,
                detect_language_by_mse,
                detect_language_by_top_n,
                get_top_n_words,
                remove_stop_words,
                save_profile,
                tokenize)

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
    unk_profile = create_language_profile("unknown", unknown_text, stopwords)
    de_profile = create_language_profile("de", de_text, stopwords)
    en_profile = create_language_profile("en", en_text, stopwords)
    checks = [check_profile(unk_profile), check_profile(de_profile), check_profile(en_profile)]
    if not all(checks):
        result = None
    print(get_top_n_words(calculated_frequencies, 7))
    print(detect_language_by_top_n(unk_profile, en_profile, de_profile, 15))
    print(detect_language_by_mse(unk_profile, en_profile, de_profile))
    save_profile(unk_profile, 'lab_1_classify_profile/assets/profiles')
    save_profile(de_profile, 'lab_1_classify_profile/assets/profiles')
    save_profile(en_profile, 'lab_1_classify_profile/assets/profiles')
    list_of_paths = ['lab_1_classify_profile/assets/profiles/unknown.json',
                     'lab_1_classify_profile/assets/profiles/de.json',
                     'lab_1_classify_profile/assets/profiles/en.json']
    result = collect_profiles(list_of_paths)
    assert result, "Detection result is None"
    return result

if __name__ == "__main__":
    print(main())

