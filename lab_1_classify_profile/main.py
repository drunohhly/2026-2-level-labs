"""
Lab 1.

Language detection
"""
# pylint:disable=unused-argument
from typing import Sequence
import re

FreqDictType = dict[str, float]
"Frequency dictionary. Contains pairs of token and its frequency."
ProfileType = tuple[str, FreqDictType, int]
"Language profile of a text. Contains language name, frequency dictionary and number of tokens."
# Mark 4.



def tokenize(text: str) -> Sequence[str] | None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words

    Args:
       text (str): Text

    Returns:
        Sequence[str] | None: Sequence of lower-cased tokens without punctuation.
        Returns None if input text is not a string.
    """
    if not isinstance(text, str):
        return None
    else:
        text = text.lower
        text = re.sub(r"[^\w\s]", "", text())
        text = re.sub(r"\d", "", text)
        tokens = [word for word in text.split()]
        return tokens

def remove_stop_words(tokens: Sequence[str], stop_words: Sequence[str]) -> Sequence[str] | None:
    """
    Removes stop words

    Args:
        tokens (Sequence[str]): Sequence of tokens
        stop_words (Sequence[str]): Sequence of stop words (can be empty)
    Returns:
        Sequence[str] | None: Sequence of tokens without stop words.
        Returns None in case of incorrect input types.
    """
    checks = [isinstance(tokens, list), isinstance(stop_words, list)]
    if not all(checks):
        return None
    for element in tokens:
        if not isinstance(element, str):
            return None
    for el in stop_words:
        if not isinstance(el, str):
            return None
    else:
        for _ in tokens:
            cleaned_text = [word for word in tokens if word not in stop_words]
        return cleaned_text


def calculate_frequencies(tokens: Sequence[str]) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens

    Args:
        tokens (Sequence[str]): Sequence of tokens
    Returns:
        dict[str, float] | None: Dictionary with frequencies.
        Returns None in case of incorrect input types.
    """
    if not isinstance(tokens, list):
        return None
    for element in tokens:
        if not isinstance(element, str):
            return None
    else:
        frequency = {}
        overall_words = len(tokens)
        for element in tokens:
            if element not in frequency:
                frequency[element] = 1
            else:
                frequency[element] = frequency[element] + 1
        for element in frequency:
            frequency[element] = frequency[element] / overall_words
        return frequency


def get_top_n_words(freq_dict: dict[str, float], top_n: int) -> Sequence[str] | None:
    """
    Finds the most common words

    Args:
        freq_dict (dict[str, float]): Dictionary with frequencies
        top_n (int): Number of the most common words

    Returns:
        Sequence[str] | None: Sequence of the most common words.
        Returns None in case of incorrect input types or non-positive top_n.
    """
    checks = [isinstance(freq_dict, dict), isinstance(top_n, int), top_n >0]
    if not all(checks):
             return None
    for key, value in freq_dict.items():
        if not (isinstance(key, str) and (isinstance(value, float))):
            return None
    else:
        freq_dict_k = freq_dict.keys()
        freq_dict_v = freq_dict.values()
        freq_dict = zip(freq_dict_v, freq_dict_k)
        sorted_freq_dict = sorted(freq_dict, key = lambda x: (-x[0], x[1]))
        sorted_freq_list = list(sorted_freq_dict[:top_n])
        sorted_freq_list = [element[1] for element in sorted_freq_list]
        return sorted_freq_list


# Mark 6.


def create_language_profile(
    language: str, text: str, stop_words: Sequence[str]
) -> ProfileType | None:
    """
    Creates a language profile

    Args:
        language (str): Language name
        text (str): Text
        stop_words (Sequence[str]): Sequence of stop words (can be empty)

    Returns:
        ProfileType | None: Language profile.
        Returns None in case of incorrect input types.
    """
    checks = [isinstance(language, str), isinstance(text, str), isinstance(stop_words, list)]
    if not all(checks):
         return None
    else:
        tokenized_text = tokenize(text)
        if not isinstance(tokenized_text, list):
             return None
        for el in tokenized_text:
                if not isinstance(el, str):
                    return None
    tokenized_text_without_stopwords = remove_stop_words(tokenized_text, stop_words)
    if not isinstance(tokenized_text_without_stopwords, list):
             return None
    for element in tokenized_text_without_stopwords:
        if not isinstance(element, str):
            return None
    freq_dict = calculate_frequencies(tokenized_text_without_stopwords)
    if not isinstance(freq_dict, dict):
        return None
    for elem in freq_dict:
        checks_2 = [isinstance(elem, str), isinstance(freq_dict[elem], float) ]
        if sum(checks_2) < 2:
            return None
        else:
            sorted_freq_dict = dict(sorted(freq_dict.items()))
            frequency = {}
            for element in tokenized_text_without_stopwords:
                if element not in frequency:
                    frequency[element] = 1
                else:
                    frequency[element] = frequency[element] + 1
            for element in frequency:
                if frequency[element] == 1:
                    freq_unique_list = [element for element in frequency]
                    n_words = len(freq_unique_list)
                    lang_profile = (language, sorted_freq_dict, n_words)
                    return lang_profile

def check_profile(profile: ProfileType) -> bool:
    """
    Checks profile structure

    Args:
        profile (ProfileType): Profile to check

    Returns:
        bool: Returns True if the profile has right structure and types,
        otherwise returns False.
    """
    if not isinstance(profile, tuple):
        return False
    elif not len(profile) == 3:
        return False
    checks = [isinstance(profile[0], str), isinstance(profile[1], dict), isinstance(profile[2], int)]
    if not all (checks):
        return False
    for keys, values in profile[1].items():
        if not (isinstance(keys, str) and isinstance(values, float)):
            return False
    else:
         return True

def compare_profiles_by_top_n(
    unknown_profile: ProfileType, profile_to_compare: ProfileType, top_n: int
) -> float | None:
    """
    Compares profiles and calculates the distance using top n words

    Args:
        unknown_profile (ProfileType): Unknown profile
        profile_to_compare (ProfileType): Profile of a known language
        top_n (int): Number of the most common words
    Returns:
        float | None: The distance between profiles.
        Returns None in case of incorrect input types.
    """
    checks = [check_profile(unknown_profile), check_profile (profile_to_compare)]
    if not all(checks):
        return None
    if not isinstance(top_n, int):
        return None
    if top_n <= 0:
        return None
    else:
        freq_dict_unk = unknown_profile[1]
        freq_dict_sec = profile_to_compare[1]
        top_words_unk = get_top_n_words(freq_dict_unk, top_n)
        if not isinstance(top_words_unk, list):
            return None
        top_words_sec = get_top_n_words(freq_dict_sec, top_n)
        if not isinstance(top_words_sec, list):
                    return None
        list_of_common_words = [word for word in top_words_unk if word in top_words_sec]
        num_of_common_words = len(list_of_common_words)
        num_of_unk_words = len(top_words_unk)
        proportion_of_overlapping_words = num_of_common_words / num_of_unk_words
        return proportion_of_overlapping_words

def detect_language_by_top_n(
    unknown_profile: ProfileType, profile_1: ProfileType, profile_2: ProfileType, top_n: int
) -> str | None:
    """
    Detects the language of an unknown profile

    Args:
        unknown_profile (ProfileType): Unknown profile
        profile_1 (ProfileType): Profile for comparison
        profile_2 (ProfileType): Another profile for comparison
        top_n (int): Number of the most common words

    Returns:
        str | None: Unknown profile language.
        Returns None in case of incorrect input types.
    """
    if not isinstance(top_n, int) or top_n <= 0:
        return None
    checks = [check_profile(unknown_profile), check_profile(profile_1), check_profile(profile_2)]
    if not all(checks):
        return None
    compared = [compare_profiles_by_top_n(unknown_profile, profile_1, top_n), compare_profiles_by_top_n(unknown_profile, profile_2, top_n)]
    for element in compared:
        if not isinstance(element, float):
            return None
    if compared[0] > compared[1]:
        return profile_1[0]
    if compared[0] < compared[1]:
            return profile_2[0]
    if compared[0] == compared[1]:
        list_of_langs = [profile_1[0], profile_2[0]]
        sorted_list = sorted(list_of_langs)
        return sorted_list[0]


# Mark 8


def calculate_mse(predicted: Sequence[float], actual: Sequence[float]) -> float | None:
    """
    Calculates mean squared error between predicted and actual values.

    Args:
        predicted (Sequence[float]): Sequence of predicted values
        actual (Sequence[float]): Sequence of actual values

    Returns:
        float | None: The score
        Returns None in case of incorrect input types or mismatched length.
        In case of empty inputs, returns 0.0.
    """
    checks = [isinstance(predicted, list), isinstance(actual, list)]
    if not all(checks):
        return None
    if len(predicted) != len(actual):
        return None
    if len(predicted) == 0 or len(actual) == 0:
        return 0.0
    for element in predicted:
        if not isinstance(element, float):
            return None
    for el in actual:
        if not isinstance(el, float):
            return None
    dict_of_values = dict(zip(actual, predicted))
    diffs = []
    for elem in dict_of_values:
        diff = (elem - dict_of_values[elem])**2
        diffs.append(diff)
    summ = sum(diffs)
    mse = summ / len(actual)
    return mse

def compare_profiles_by_mse(
    unknown_profile: ProfileType, profile_to_compare: ProfileType
) -> float | None:
    """
    Compares two language profiles using the MSE metric.

    Args:
        unknown_profile (ProfileType): Unknown profile
        profile_to_compare (ProfileType): Profile
            to compare the unknown profile with

    Returns:
        float | None: The distance between the profiles.
        In case of corrupt input arguments or invalid profile structure, None is returned.
    """
    checks = [check_profile(unknown_profile), check_profile (profile_to_compare)]
    if not all(checks):
        return None
    list_of_unk = []
    list_of_second = []
    list_of_tokens = []
    for element in unknown_profile[1]:
        list_of_tokens.append(element)
        list_of_unk.append(element)
    for el in profile_to_compare[1]:
            if el not in list_of_tokens:
                list_of_tokens.append(el)
            list_of_second.append(el)
    list_of_mse_unk = []
    for elem in list_of_tokens:
        if elem in list_of_unk:
            list_of_mse_unk.append(unknown_profile[1][elem])
        else:
            list_of_mse_unk.append(0.0)
    list_of_mse_sec = []
    for ele in list_of_tokens:
            if ele in list_of_second:
                list_of_mse_sec.append(profile_to_compare[1][ele])
            else:
                list_of_mse_sec.append(0.0)
    result = calculate_mse(list_of_mse_unk, list_of_mse_sec)
    return result

def detect_language_by_mse(
    unknown_profile: ProfileType, profile_1: ProfileType, profile_2: ProfileType
) -> str | None:
    """
    Detects the language of an unknown profile.

    Args:
        unknown_profile (ProfileType): Profile
            to determine the language of
        profile_1 (ProfileType): Known profile
        profile_2 (ProfileType): Another known profile

    Returns:
        str | None: Unknown profile language.
        Returns None in case of incorrect input types.
    """
    checks = [check_profile(unknown_profile), check_profile(profile_1), check_profile(profile_2)]
    if not all(checks):
        return None
    checks_2 = [compare_profiles_by_mse(unknown_profile, profile_1), compare_profiles_by_mse(unknown_profile, profile_2)]
    for element in checks_2:
        if not isinstance(element, float):
            return None
    if checks_2[0] > checks_2[1]:
        return profile_2[0]
    if checks_2[0] < checks_2[1]:
        return profile_1[0]
    if checks_2[0] == checks_2[1]:
        list_of_langs = [profile_1[0], profile_2[0]]
        sorted_list = sorted(list_of_langs)
        return sorted_list[0]

# Mark 10


def save_profile(profile: ProfileType, save_path: str) -> bool:
    """
    Saves a language profile

    Args:
        profile (ProfileType): Profile
        save_path (str): Path to the folder to save profile

    Returns:
        bool: False in case of incorrect input types or if the profile
        is missing obligatory keys. True if the profile is saved.
    """


def load_profile(path_to_file: str) -> ProfileType | None:
    """
    Loads a language profile.

    Args:
        path_to_file (str): Path to the language profile

    Returns:
        ProfileType | None: Loaded profile.
        Returns None in case of incorrect input types.
    """


def collect_profiles(paths_to_profiles: Sequence[str]) -> Sequence[ProfileType] | None:
    """
    Collects profiles for a given path.

    Args:
        paths_to_profiles (Sequence[str]): Sequence of paths to the profiles

    Returns:
        Sequence[ProfileType] | None: Sequence of loaded profiles.
        Returns None in case of incorrect input types.
    """


def detect_language_advanced(
    unknown_profile: ProfileType, known_profiles: Sequence[ProfileType], top_n: int
) -> Sequence[tuple[str, dict[str, float]]] | None:
    """
    Detects the language of an unknown profile.

    Args:
        unknown_profile (ProfileType): Profile
            to determine the language of
        known_profiles (Sequence[ProfileType]): Known profiles
        top_n (int): Number of popular words

    Returns:
        Sequence[tuple[str, dict[str, float]]] | None: Sorted sequence of tuples
        containing a language and a distance via both metrics.
        The sequence is sorted by best MSE value, then by best Top-N value.
        Returns None in case of incorrect input types.
    """


def print_report(
    unknown_profile: ProfileType, metrics_stats: Sequence[tuple[str, dict[str, float]]], top_n: int
) -> None:
    """
    Prints report for detection of language.

    Args:
        unknown_profile (ProfileType): Profile
        metrics_stats (Sequence[tuple[str, dict[str, float]]]): Sequence with distances for
            available language comparison and metrics
        top_n (int): Number of popular words

    In case of incorrect type inputs, does not print anything.
    """
