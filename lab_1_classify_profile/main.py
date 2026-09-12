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
    if isinstance(text, str) == False:
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
    if isinstance(tokens, list) == False or isinstance(stop_words, list) == False:
        return None
    for element in tokens:
        if isinstance(element, str) == False:
            return None
    for el in stop_words:
        if isinstance(el, str) == False:
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
    if isinstance(tokens, list) == False:
        return None
    for element in tokens:
        if isinstance(element, str) == False:
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
    if isinstance(freq_dict, dict) != True or isinstance(top_n, int) != True or top_n <= 0:
             return None
    for element in freq_dict:
        if isinstance(element, str) != True:
            return None
    else:
        for element in freq_dict:
            if isinstance(freq_dict[element], float) != True:
                if isinstance(freq_dict[element], str) == True and freq_dict[element].isdigit():
                    freq_dict[element] = float(freq_dict[element])
                if isinstance(freq_dict[element], int) == True:
                    freq_dict[element] = float(freq_dict[element])
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
    if isinstance(language, str) != True or isinstance(text, str) != True or isinstance(stop_words, list) != True:
         return None
    else:
        tokenized_text = tokenize(text)
        if isinstance(tokenized_text, list) != True:
             return None
        for el in tokenized_text:
                if isinstance(el, str) != True:
                    return None

        tokenized_text_without_stopwords = remove_stop_words(tokenized_text, stop_words)

        if isinstance(tokenized_text_without_stopwords, list) != True:
             return None
        for element in tokenized_text_without_stopwords:
             if isinstance(element, str) != True:
                  return None

        freq_dict = calculate_frequencies(tokenized_text_without_stopwords)

        if isinstance(freq_dict, dict) != True:
                 return None
        for elem in freq_dict:
            if isinstance(elem, str) != True or isinstance(freq_dict[elem], float) != True:
                return None

        else:
            sorted_freq_dict = dict(sorted(freq_dict.items()))
            #absolute frequency:
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


def check_profile(profile: ProfileType) -> bool:
    if  isinstance(profile, tuple) != True:
         return False
    elif isinstance(profile[0], str) != True:
        return False
    elif isinstance(profile[1], dict) != True:
        return False
    elif isinstance(profile[2], int) != True:
        return False
    else:
         return True

"""
    Checks profile structure

    Args:
        profile (ProfileType): Profile to check

    Returns:
        bool: Returns True if the profile has right structure and types,
        otherwise returns False.
    """


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
