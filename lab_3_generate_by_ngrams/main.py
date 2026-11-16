"""
Lab 3.
Beam-search and natural language generation evaluation
"""
import json
import math

# pylint:disable=too-few-public-methods

import json
import math


class TextProcessor:
    """
    Handle text tokenization, encoding and decoding.

    Attributes:
        _end_of_word_token (str): A token denoting word boundary
        _storage (dict): Dictionary in the form of <token: identifier>
    """
    def __init__(self, end_of_word_token: str) -> None:
        """
        Initialize an instance of TextProcessor.

        Args:
            end_of_word_token (str): A token denoting word boundary
        """
        if (
            not isinstance(end_of_word_token, str)
            or not end_of_word_token
        ):
            return

        self._end_of_word_token = end_of_word_token
        self._storage = {end_of_word_token: 0}

    def _tokenize(self, text: str) -> tuple[str, ...] | None:
        """
        Tokenize text into unigrams, separating words with special token.

        Punctuation and digits are removed. EoW token is appended after the last word in two cases:
        1. It is followed by punctuation
        2. It is followed by space symbol

        Args:
            text (str): Original text

        Returns:
            tuple[str, ...] | None: Tokenized text

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not isinstance(text, str):
            return None

        tokens = []
        words = text.split()
        valid_words = sum(1 for word in words if any(symb.isalpha() for symb in word))

        words_processed = 0
        for word in words:
            cleaned_word = [symb.lower() for symb in word if symb.isalpha()]
            if not cleaned_word:
                continue

            tokens.extend(cleaned_word)
            words_processed += 1

            if words_processed < valid_words or not text[-1].isalpha():
                tokens.append(self._end_of_word_token)

        if not tokens:
            return None

        return tuple(tokens)

        if text.isdigit():
            return None

        text = text.lower()
        for element in text[:-1]:
            if not (element.isalpha() or element == " " or element == "\n"):
                text = text.replace(element, "")

        text = text.replace(" ", self._end_of_word_token)
        text = text.replace("\n", self._end_of_word_token)

        while f"{self._end_of_word_token}{self._end_of_word_token}" in text:
            text = text.replace(f"{self._end_of_word_token}{self._end_of_word_token}",
                                f"{self._end_of_word_token}")

        if not text[-1].isalpha():
            text = text.replace(text[-1], self._end_of_word_token)
        result = list(text)
        return tuple(result)
    def get_id(self, element: str) -> int | None:
        """
        Retrieve a unique identifier of an element.

        Args:
            element (str): String element to retrieve identifier for

        Returns:
            int | None: Integer identifier that corresponds to the given element

        In case of corrupt input arguments or arguments not included in storage,
        None is returned
        """
        if not isinstance(element, str) or not element:
            return None

        return self._storage.get(element)

    def get_end_of_word_token(self) -> str:  # type: ignore[empty-body]
        """
        Retrieve value stored in self._end_of_word_token attribute.

        Returns:
            str: EoW token
        """
        return self._end_of_word_token

    def get_token(self, element_id: int) -> str | None:
        """
        Retrieve an element by unique identifier.

        Args:
            element_id (int): Identifier to retrieve identifier for

        Returns:
            str | None: Element that corresponds to the given identifier

        In case of corrupt input arguments or arguments not included in storage, None is returned
        """
        if not isinstance(element_id, int):
            return None

        for el, el_id in self._storage.items():
            if el_id == element_id:
                return el

        return None

    def encode(self, text: str) -> tuple[int, ...] | None:
        """
        Encode text.

        Tokenize text, assign each symbol an integer identifier and
        replace letters with their ids.

        Args:
            text (str): An original text to be encoded

        Returns:
            tuple[int, ...] | None: Processed text

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not isinstance(text, str) or not text:
            return None

        tokens = self._tokenize(text)
        if tokens is None:
            return None

        encoded_corpus = []
        for symb in tokens:
            self._put(symb)
            if (symb_id := self.get_id(symb)) is None:
                return None
            encoded_corpus.append(symb_id)

        return tuple(encoded_corpus)

        tokens = self._tokenize(text)
        if not isinstance(tokens, tuple):
            return None

        for element in tokens:
            if element not in self._storage:
                self._put(element)

        list_of_id = []
        for element in tokens:
            element_id = self.get_id(element)
            if not isinstance(element_id, int):
                return None

            list_of_id.append(element_id)
        return tuple(list_of_id)
    def _put(self, element: str) -> None:
        """
        Put an element into the storage, assign a unique id to it.

        Args:
            element (str): An element to put into storage

        In case of corrupt input arguments or invalid argument length,
        an element is not added to storage
        """
        if not isinstance(element, str) or len(element) != 1:
            return

        if element not in self._storage:
            self._storage[element] = len(self._storage)

    def decode(self, encoded_corpus: tuple[int, ...]) -> str | None:
        """
        Decode and postprocess encoded corpus by converting integer identifiers to string.

        Special symbols are replaced with spaces (no multiple spaces in a row are allowed).
        The first letter is capitalized, resulting sequence must end with a full stop.

        Args:
            encoded_corpus (tuple[int, ...]): A tuple of encoded tokens

        Returns:
            str | None: Resulting text

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not isinstance(encoded_corpus, tuple):
            return None

        for symb in encoded_corpus:
            if not isinstance(symb, int):
                return None

        decoded = self._decode(encoded_corpus)
        if decoded is None:
            return None

        return self._postprocess_decoded_text(decoded)

        if not encoded_corpus:
            return None

        decoded_corpus = self._decode(encoded_corpus)
        if not decoded_corpus:
            return None
        text = self._postprocess_decoded_text(decoded_corpus)
        if not text:
            return None
        return text
    def fill_from_ngrams(self, content: dict) -> None:
        """
        Fill internal storage with letters from external JSON.

        Args:
            content (dict): ngrams from external JSON
        """
        if not isinstance(content, dict) or not content:
            return
        if not isinstance(content.get("freq"), dict):
            return
        if not all(isinstance(ngram, str) for ngram in content.get("freq")):
            return

        for ngram in content.get("freq"):
            for symb in ngram:
                if symb.isalpha():
                    self._put(symb.lower())

        if not content:
            return None

        for key in list(content.values())[0]:
            for letter in key:
                if letter.isalpha():
                    if letter.lower() in self._storage:
                        continue
                    self._put(letter.lower())
        return None
    def _decode(self, corpus: tuple[int, ...]) -> tuple[str, ...] | None:
        """
        Decode sentence by replacing ids with corresponding letters.

        Args:
            corpus (tuple[int, ...]): A tuple of encoded tokens

        Returns:
            tuple[str, ...] | None: Sequence with decoded tokens

        In case of corrupt input arguments, None is returned.
        In case any of methods used return None, None is returned.
        """
        if not isinstance(corpus, tuple) or not corpus:
            return None

        for symb in corpus:
            if not isinstance(symb, int) or isinstance(symb, bool):
                return None

        decoded_corpus = []
        for el_id in corpus:
            el = self.get_token(el_id)
            if el is None:
                return None
            decoded_corpus.append(el)

        return tuple(decoded_corpus)

        if not corpus or not all(isinstance(i, int) for i in corpus):
            return None

        list_of_tokens = []
        for element in corpus:
            token = self.get_token(element)

            if token is None:
                return None
            list_of_tokens.append(token)
        return tuple(list_of_tokens)
    def _postprocess_decoded_text(self, decoded_corpus: tuple[str, ...]) -> str | None:
        """
        Convert decoded sentence into the string sequence.

        Special symbols are replaced with spaces (no multiple spaces in a row are allowed).
        The first letter is capitalized, resulting sequence must end with a full stop.

        Args:
            decoded_corpus (tuple[str, ...]): A tuple of decoded tokens

        Returns:
            str | None: Resulting text

        In case of corrupt input arguments, None is returned
        """
        if not isinstance(decoded_corpus, tuple):
            return None
        for symb in decoded_corpus:
            if not isinstance(symb, str):
                return None

        decoded_element = ""
        for el in decoded_corpus:
            if el == self._end_of_word_token:
                if decoded_element and not decoded_element.endswith(" "):
                    decoded_element += " "
            else:
                decoded_element += el
        decoded_element = decoded_element.strip()
        if not decoded_element:
            return None

        return decoded_element.capitalize() + "."

        if not decoded_corpus:
            return None

        text = ""
        for element in decoded_corpus:
            text = f"{text}{element}"
        if self._end_of_word_token in text[:-1]:
            text = text[:-1].replace(self._end_of_word_token, " ")

        text = text.capitalize()
        if text[-1] == self._end_of_word_token:
            text = text.replace(self._end_of_word_token, ".")
        else:
            text = f"{text}."
        return text
class WordProcessor(TextProcessor):
    """
    Handle text tokenization, encoding and decoding on the level of words.

    Attributes:
        _end_of_word_token (str): A token denoting sentence boundary
        _storage (dict): Dictionary in the form of <token: identifier>
    """
    def _tokenize(self, text: str) -> tuple[str, ...] | None:
        """
        Tokenize text into words, separating sentences with special token.

        Punctuation and digits are removed. Special token is appended after the word
        that ends a sentence, i.e. is followed by '.', '!' or '?'.

        Args:
            text (str): Original text

        Returns:
            tuple[str, ...] | None: Tokenized text

        In case of corrupt input arguments, None is returned.
        In case text does not contain any words, None is returned.
        """
        if not isinstance(text, str) or not text:
            return None

        tokens = []
        end_tokens = ('.', '?', '!')

        for word in text.lower().split():
            sentence_end = word.endswith(end_tokens)
            clean_word = ''.join(symb for symb in word if symb.isalpha())
            if clean_word:
                tokens.append(clean_word)

            if sentence_end and tokens and tokens[-1] != self._end_of_word_token:
                tokens.append(self._end_of_word_token)
        if not tokens:
            return None

        return tuple(tokens)

        if any([not text, text.isdigit()]):
            return None

        syms_to_del = [".", "?", "!"]
        preprocessed_text = text.lower()
        for sym in syms_to_del:
            preprocessed_text = preprocessed_text.replace(sym, self._end_of_word_token)

        while f"{self._end_of_word_token}{self._end_of_word_token}" in preprocessed_text:
            preprocessed_text = preprocessed_text.replace(
                                            f"{self._end_of_word_token}{self._end_of_word_token}",
                                            f"{self._end_of_word_token}")

        if f"{self._end_of_word_token}" in preprocessed_text:
            preprocessed_text = preprocessed_text.replace(f"{self._end_of_word_token}",
                                                        f" {self._end_of_word_token}")

        for letter in preprocessed_text:
            if not any([letter.isalpha(),
                        letter in self._end_of_word_token,
                        letter == " ",
                        letter == "'"]):
                preprocessed_text = preprocessed_text.replace(letter, " ")
            if letter == "'":
                preprocessed_text = preprocessed_text.replace(letter, "")
        result = tuple(preprocessed_text.split())

        list_of_letters = []
        for token in result:
            if not token.isalpha():
                continue
            list_of_letters.append(token)
        if not list_of_letters:
            return None
        return result
    def _put(self, element: str) -> None:
        """
        Put a word into the storage, assign a unique id to it.

        Args:
            element (str): A word to put into storage

        In case of corrupt input arguments, an element is not added to storage
        """
        if not isinstance(element, str) or not element:
            return
        if element not in self._storage:
            self._storage[element] = len(self._storage)

    def _postprocess_decoded_text(self, decoded_corpus: tuple[str, ...]) -> str | None:
        """
        Convert decoded sequence of words into the string sequence.

        Words are separated with spaces, special tokens are replaced with full stops.
        Each sentence is capitalized, resulting sequence must end with a full stop.

        Args:
            decoded_corpus (tuple[str, ...]): A tuple of decoded tokens

        Returns:
            str | None: Resulting text

        In case of corrupt input arguments, None is returned.
        In case decoded corpus does not contain any words, None is returned.
        """
        if (
            not isinstance(decoded_corpus, tuple)
            or not decoded_corpus
            or not all(isinstance(token, str) for token in decoded_corpus)
        ):
            return None

        sentences = []
        current_sentence = []
        for token in decoded_corpus:
            if token == self._end_of_word_token:
                if current_sentence:
                    sentence = ' '.join(current_sentence).capitalize()
                    sentences.append(sentence)
                    current_sentence = []
            else:
                current_sentence.append(token)

        if current_sentence:
            sentence = ' '.join(current_sentence).capitalize()
            sentences.append(sentence)
        if not sentences:
            return None

        return f'{'. '.join(sentences)}.'

        text = " ".join(decoded_corpus)
        text = text.replace(f" {self._end_of_word_token}", ".")

        sentences = text.split(". ")
        text = ". ".join(s.capitalize() for s in sentences)
        if not text.endswith("."):
            text += "."
        return text

class NGramLanguageModel:
    """
    Store language model by n_grams, predict the next token.

    Attributes:
        __n_gram_size (int): A size of n-grams to use for language modelling
        _n_gram_frequencies (dict): Frequencies for n-grams
        _encoded_corpus (tuple): Encoded text
    """
    def __init__(self, encoded_corpus: tuple | None, n_gram_size: int) -> None:
        """
        Initialize an instance of NGramLanguageModel.

        Args:
            encoded_corpus (tuple | None): Encoded text
            n_gram_size (int): A size of n-grams to use for language modelling
        """
        self._encoded_corpus = encoded_corpus
        self.__n_gram_size = n_gram_size
        self._n_gram_frequencies = {}

    def get_n_gram_size(self) -> int:  # type: ignore[empty-body]
        """
        Retrieve value stored in self.__n_gram_size attribute.

        Returns:
            int: Size of stored n_grams
        """
        return self.__n_gram_size

    def set_n_grams(self, frequencies: dict) -> None:
        """
        Setter method for n-gram frequencies.

        Args:
            frequencies (dict): Computed in advance frequencies for n-grams
        """
        if not isinstance(frequencies, dict) or not frequencies:
            return
        self._n_gram_frequencies = frequencies

    def build(self) -> bool:
        """
        Fill attribute `_n_gram_frequencies` from encoded corpus.

        Encoded corpus is stored in the attribute `_encoded_corpus`

        Returns:
            bool: True if attribute is filled successfully, otherwise False

        In case of corrupt input arguments or methods used return None,
        False is returned
        """
        if not isinstance(self._encoded_corpus, tuple) or not self._encoded_corpus:
            return False
        if not all(isinstance(number, int) for number in self._encoded_corpus):
            return False
        if not isinstance(self.__n_gram_size, int) or self.__n_gram_size < 1:
            return False

        n_grams = self._extract_n_grams(self._encoded_corpus)
        if n_grams is None:
            return False

        absolute_freq = {}
        for n_gram in n_grams:
            absolute_freq[n_gram] = absolute_freq.get(n_gram, 0) + 1

        same_start_freq = {}
        for n_gram, freq in absolute_freq.items():
            context = n_gram[:-1]
            same_start_freq[context] = same_start_freq.get(context, 0) + freq

        frequencies = {}
        for n_gram, freq in absolute_freq.items():
            context = n_gram[:-1]
            frequencies[n_gram] = freq / same_start_freq[context]
        self._n_gram_frequencies = frequencies

        return True

        if not self._encoded_corpus:
            return False

        corpus_of_n_gramms = self._extract_n_grams(self._encoded_corpus)
        if not corpus_of_n_gramms:
            return False

        dict_of_frequency = {}
        for n_gramm in corpus_of_n_gramms:
            dict_of_frequency[n_gramm] = dict_of_frequency.get(n_gramm, 0) + 1

        corpus_of_starts = []
        for item in corpus_of_n_gramms:
            n_gram = list(item)
            n_gram.pop(-1)
            corpus_of_starts.append(tuple(n_gram))

        dict_of_freq_starts = {}
        for item in corpus_of_starts:
            dict_of_freq_starts[item] = dict_of_freq_starts.get(item, 0) + 1

        for n_gramm in set(corpus_of_n_gramms):
            context = n_gramm[:-1]
            mle = dict_of_frequency[n_gramm] / dict_of_freq_starts[context]
            self._n_gram_frequencies[n_gramm] = mle

        if not self._n_gram_frequencies:
            return False
        return True
    def generate_next_token(self, sequence: tuple[int, ...]) -> dict | None:
        """
        Retrieve tokens that can continue the given sequence along with their probabilities.

        Args:
            sequence (tuple[int, ...]): A sequence to match beginning of NGrams for continuation

        Returns:
            dict | None: Possible next tokens with their probabilities

        In case of corrupt input arguments, None is returned
        """
        if not isinstance(sequence, tuple) or not sequence:
            return None
        if not self._n_gram_frequencies:
            return None

        context_length = self.__n_gram_size - 1
        if len(sequence) < context_length:
            return None

        context = sequence[-context_length:]
        next_tokens_freq = {}
        for n_gram, freq in self._n_gram_frequencies.items():
            if n_gram[:-1] == context:
                next_tokens_freq[n_gram[-1]] = freq
        if next_tokens_freq is None:
            return None

        return next_tokens_freq

        if not sequence:
            return None

        if len(sequence) < self.__n_gram_size - 1:
            return None

        context = sequence[-self.__n_gram_size + 1:]
        n_gramms = list(self._n_gram_frequencies.keys())
        corpus_of_possible_token = []
        for n_gramm in n_gramms:
            if context == n_gramm[:self.__n_gram_size - 1]:
                corpus_of_possible_token.append(n_gramm)

        dict_of_predictions = {}
        for item in corpus_of_possible_token:
            dict_of_predictions[item[-1]] = self._n_gram_frequencies.get(item)

        return dict_of_predictions
    def _extract_n_grams(
        self, encoded_corpus: tuple[int, ...]
    ) -> tuple[tuple[int, ...], ...] | None:
        """
        Split encoded sequence into n-grams.

        Args:
            encoded_corpus (tuple[int, ...]): A tuple of encoded tokens

        Returns:
            tuple[tuple[int, ...], ...] | None: A tuple of extracted n-grams

        In case of corrupt input arguments, None is returned
        """
        if not isinstance(encoded_corpus, tuple) or not encoded_corpus:
            return None
        if self.__n_gram_size > len(encoded_corpus):
            return None

        n_grams = []
        for i in range(len(encoded_corpus) - self.__n_gram_size + 1):
            n_gram = encoded_corpus[i:i + self.__n_gram_size]
            n_grams.append(n_gram)

        return tuple(n_grams)

        if not encoded_corpus:
            return None

        corpus = list(encoded_corpus)
        res = tuple(tuple(corpus[i:i + self.__n_gram_size])
                for i in range(len(corpus) - self.__n_gram_size + 1))
        return res
class GreedyTextGenerator:
    """
    Greedy text generation by N-grams.

    Attributes:
        _model (NGramLanguageModel): A language model to use for text generation
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
    """
    def __init__(self, language_model: NGramLanguageModel, text_processor: TextProcessor) -> None:
        """
        Initialize an instance of GreedyTextGenerator.

        Args:
            language_model (NGramLanguageModel): A language model to use for text generation
            text_processor (TextProcessor): A TextProcessor instance to handle text processing
        """
        self._model = language_model
        self._text_processor = text_processor

    def run(self, prompt: str, seq_len: int) -> str | None:
        """
        Generate sequence based on NGram language model and prompt provided.

        Args:
            prompt (str): Beginning of sequence
            seq_len (int): Number of tokens to generate

        Returns:
            str | None: Generated sequence

        In case of corrupt input arguments or methods used return None,
        None is returned
        """
        if not isinstance(prompt, str) or not isinstance(seq_len, int):
            return None
        if seq_len <= 0:
            return None

        encoded_prompt = self._text_processor.encode(prompt)
        if encoded_prompt is None:
            return None

        sequence = list(encoded_prompt)
        for _ in range(seq_len):
            next_tokens = self._model.generate_next_token(tuple(sequence))
            if not next_tokens:
                break
            best_token = max((score, token) for token, score in next_tokens.items())[1]
            sequence.append(best_token)
        generated_sequence = tuple(sequence)

        return self._text_processor.decode(generated_sequence)

        if not all([prompt, seq_len]):
            return None

        if seq_len <= 0:
            return None

        encoded_text = self._text_processor.encode(prompt)
        if not encoded_text:
            return None

        sequence = list(encoded_text)

        for _ in range(seq_len + 1):
            dict_of_predicted = self._model.generate_next_token(tuple(sequence))
            if not dict_of_predicted:
                break
            pred = sorted(dict_of_predicted.items(), key = lambda x: (x[1], x[0]), reverse = True)
            sequence.append(pred[0][0])
        text = self._text_processor.decode(tuple(sequence))
        if not text:
            return None
        return text
class BeamSearcher:
    """
    Beam Search algorithm for diverse text generation.

    Attributes:
        _beam_width (int): Number of candidates to consider at each step
        _model (NGramLanguageModel): A language model to use for next token prediction
    """
    def __init__(self, beam_width: int, language_model: NGramLanguageModel) -> None:
        """
        Initialize an instance of BeamSearcher.

        Args:
            beam_width (int): Number of candidates to consider at each step
            language_model (NGramLanguageModel): A language model to use for next token prediction
        """
        self._beam_width = beam_width
        self._model = language_model

    def get_next_token(self, sequence: tuple[int, ...]) -> list[tuple[int, float]] | None:
        """
        Retrieve candidate tokens for sequence continuation.

        Candidates are sorted by probability and then by token in descending order.
        Number of tokens retrieved must not be bigger than beam width parameter.

        The return value has the following format: [(token, probability), ...].

        Args:
            sequence (tuple[int, ...]): Base sequence to continue

        Returns:
            list[tuple[int, float]] | None: Tokens to use for base sequence continuation

        In case of corrupt input arguments or methods used return None.
        """
        if not isinstance(sequence, tuple) or not sequence:
            return None

        next_tokens = self._model.generate_next_token(sequence)
        if next_tokens is None:
            return None
        if not next_tokens:
            return []
        tokens_to_use = sorted(next_tokens.items(), key=lambda x: (-x[1], -x[0]))

        return tokens_to_use[:self._beam_width]

        if not all([sequence, all(isinstance(i, int) for i in sequence)]):
            return None

        dict_of_predictions = self._model.generate_next_token(sequence)
        if not isinstance(dict_of_predictions, dict):
            return dict_of_predictions
        sorted_dict = sorted(dict_of_predictions.items(), key = lambda x: (x[1], x[0]),
                                                                        reverse = True)
        return sorted_dict[:self._beam_width]
    def continue_sequence(
        self,
        sequence: tuple[int, ...],
        next_tokens: list[tuple[int, float]],
        sequence_candidates: dict[tuple[int, ...], float],
    ) -> dict[tuple[int, ...], float] | None:
        """
        Generate new sequences from the base sequence with next tokens provided.

        The base sequence is deleted after continued variations are added.

        Args:
            sequence (tuple[int, ...]): Base sequence to continue
            next_tokens (list[tuple[int, float]]): Token for sequence continuation
            sequence_candidates (dict[tuple[int, ...], float]):
                Storage with all sequences generated

        Returns:
            dict[tuple[int, ...], float] | None: Updated sequence candidates

        In case of corrupt input arguments or unexpected behaviour of methods used return None.
        """
        if (
            not isinstance(sequence, tuple) or
            not isinstance(next_tokens, list) or
            not isinstance(sequence_candidates, dict)
        ):
            return None
        if not sequence or not next_tokens or not sequence_candidates:
            return None
        if not all(isinstance(x, int) for x in sequence):
            return None
        if len(next_tokens) > self._beam_width:
            return None
        if sequence not in sequence_candidates:
            return None

        fine = sequence_candidates[sequence]
        updated_candidates = sequence_candidates.copy()

        for token, chance in next_tokens:
            new_sequence = sequence + (token,)
            updated_candidates[new_sequence] = fine - math.log(chance)

        del updated_candidates[sequence]

        return updated_candidates

        if not all([isinstance(sequence_candidates, dict), sequence_candidates,
            len(next_tokens) <= self._beam_width]):
            return None

        if not sequence in sequence_candidates:
            return None

        for el in next_tokens:
            if not all([isinstance(el, tuple),
                isinstance(el[0], int), isinstance(el[1], float)]):
                return None

        for key, value in sequence_candidates.items():
            if not all([isinstance(key, tuple),
                        all(isinstance(token, int) for token in key),
                        isinstance(value, (int, float))
                    ]):
                return None
        dict_of_fines = {}
        for item in next_tokens:
            fine = - math.log(item[1])
            dict_of_fines[item[0]] = fine + sequence_candidates[sequence]

        candidates_for_sequence = sequence_candidates.copy()
        candidates_for_sequence.pop(sequence)
        for token, probs in dict_of_fines.items():
            continued_sequence = list(sequence)
            continued_sequence.append(token)
            candidates_for_sequence[tuple(continued_sequence)] = probs
        return candidates_for_sequence
    def prune_sequence_candidates(
        self, sequence_candidates: dict[tuple[int, ...], float]
    ) -> dict[tuple[int, ...], float] | None:
        """
        Remove those sequence candidates that do not make top-N most probable sequences.

        Args:
            sequence_candidates (dict[tuple[int, ...], float]): Current candidate sequences

        Returns:
            dict[tuple[int, ...], float] | None: Pruned sequences

        In case of corrupt input arguments return None.
        """
        if not isinstance(sequence_candidates, dict) or not sequence_candidates:
            return None

        sorted_candidates = sorted(
            sequence_candidates.items(),
            key=lambda x: (x[1], x[0])
        )

        return dict(sorted_candidates[:self._beam_width])

        if not sequence_candidates:
            return None

        for keys, values in sequence_candidates.items():
            if not all([isinstance(keys, tuple), isinstance(values, (float, int))]):
                return None
            for i in keys:
                if not isinstance(i, int):
                    return None

        sorted_dict = sorted(sequence_candidates.items(), key = lambda x: x[1])
        if len(sequence_candidates) > self._beam_width:
            sorted_dict = sorted_dict[:self._beam_width]
        return dict(sorted_dict)
class BeamSearchTextGenerator:
    """
    Class for text generation with BeamSearch.

    Attributes:
        _language_model (NGramLanguageModel): Language model for next token prediction
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
        _beam_width (int): Beam width parameter for generation
        beam_searcher (BeamSearcher): Searcher instance for the language model
    """
    def __init__(
        self, language_model: NGramLanguageModel, text_processor: TextProcessor, beam_width: int
    ) -> None:
        """
        Initializes an instance of BeamSearchTextGenerator.

        Args:
            language_model (NGramLanguageModel): Language model to use for text generation
            text_processor (TextProcessor): A TextProcessor instance to handle text processing
            beam_width (int): Beam width parameter for generation
        """
        self._language_model = language_model
        self._text_processor = text_processor
        self._beam_width = beam_width
        self.beam_searcher = BeamSearcher(
            beam_width=beam_width,
            language_model=language_model,
        )

    def run(self, prompt: str, seq_len: int) -> str | None:
        """
        Generate sequence based on NGram language model and prompt provided.

        Args:
            prompt (str): Beginning of sequence
            seq_len (int): Number of tokens to generate

        Returns:
            str | None: Generated sequence

        In case of corrupt input arguments or methods used return None,
        None is returned
        """
        if (
            not isinstance(prompt, str)
            or not prompt
            or not isinstance(seq_len, int)
            or seq_len <= 0
        ):
            return None

        encoded = self._text_processor.encode(prompt)
        if not encoded:
            return None
        seq_candidates = {encoded: 0.0}
        length = len(encoded) + seq_len

        while any(len(seq) < length for seq in seq_candidates):
            new_candidates = {}

            for seq, fine in seq_candidates.items():
                if len(seq) >= length:
                    new_candidates[seq] = fine
                    continue
                next_tokens = self._get_next_token(seq)
                if next_tokens is None:
                    return None
                if not next_tokens:
                    new_candidates[seq] = fine
                    continue

                extended_candidates = self.beam_searcher.continue_sequence(
                    sequence=seq,
                    next_tokens=next_tokens,
                    sequence_candidates={seq: fine},
                )
                if extended_candidates is None:
                    return self._text_processor.decode(seq)
                new_candidates.update(extended_candidates)

            pruned = self.beam_searcher.prune_sequence_candidates(new_candidates)
            if pruned is None:
                return None
            seq_candidates = pruned
        best_sequence = min(seq_candidates, key=lambda x: seq_candidates[x])

        return self._text_processor.decode(best_sequence)

        if not all([prompt, seq_len > 0]):
            return None

        encoded_text = self._text_processor.encode(prompt)
        if not isinstance(encoded_text, tuple):
            return None

        for _ in range(seq_len + 1):
            next_tokens = self._get_next_token(encoded_text)
            if not isinstance(next_tokens, list):
                return None

            dict_of_candidates = {encoded_text: 0.0}
            candidates_for_seq = self.beam_searcher.continue_sequence(
                                                                    encoded_text,
                                                                    next_tokens[:self._beam_width],
                                                                    dict_of_candidates
                                                                    )
            if not candidates_for_seq:
                break

            candidates = self.beam_searcher.prune_sequence_candidates(candidates_for_seq)
            if not candidates:
                return None
            encoded_text = tuple(dict(zip(candidates.values(), candidates.keys()))[(min
                                                                                (
                                                                                candidates.values()
                                                                                ))])
        return self._text_processor.decode(encoded_text)
    def _get_next_token(
        self, sequence_to_continue: tuple[int, ...]
    ) -> list[tuple[int, float]] | None:
        """
        Retrieve next tokens for sequence continuation.

        Args:
            sequence_to_continue (tuple[int, ...]): Sequence to continue

        Returns:
            list[tuple[int, float]] | None: Next tokens for sequence
            continuation

        In case of corrupt input arguments return None.
        """
        return self.beam_searcher.get_next_token(sequence_to_continue)


class NGramLanguageModelReader:
    """
    Factory for loading language models ngrams from external JSON.

    Attributes:
        _json_path (str): Local path to assets file
        _eow_token (str): Special token for text processor
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
    """
    def __init__(self, json_path: str, eow_token: str) -> None:
        """
        Initialize reader instance.

        Args:
            json_path (str): Local path to assets file
            eow_token (str): Special token for text processor
        """
        self._json_path = json_path
        self._eow_token = eow_token

        with open(self._json_path, encoding="utf-8") as json_file:
            self._content = json.load(json_file)
        self._text_processor = TextProcessor(eow_token)
        self._text_processor.fill_from_ngrams(self._content)

    def load(self, n_gram_size: int) -> NGramLanguageModel | None:
        """
        Fill attribute `_n_gram_frequencies` from dictionary with N-grams.

        The N-grams taken from dictionary must be cleaned from digits and punctuation,
        their length must match n_gram_size, and spaces must be replaced with EoW token.

        Args:
            n_gram_size (int): Size of ngram

        Returns:
            NGramLanguageModel | None: Built language model.

        In case of corrupt input arguments or unexpected behaviour of methods used,
        None is returned.
        """
        if not isinstance(n_gram_size, int) or n_gram_size < 2:
            return None
        freq_dict = self._content.get("freq")
        if not isinstance(freq_dict, dict):
            return None

        encoded_freq_dict = {}
        for ngram, freq in freq_dict.items():
            if not isinstance(ngram, str):
                return None

            tokens = [
                self._eow_token if symb.isspace() else symb.lower()
                for symb in ngram
                if symb.isspace() or symb.isalpha()
            ]
            if len(tokens) != n_gram_size:
                continue

            encoded_tokens = [
                token_id
                for token in tokens
                if (token_id := self._text_processor.get_id(token)) is not None
            ]
            if len(encoded_tokens) != n_gram_size:
                continue

            encoded_ngram = tuple(encoded_tokens)
            encoded_freq_dict[encoded_ngram] = encoded_freq_dict.get(encoded_ngram, 0) + freq

        context_frequencies = {}
        for ngram, freq in encoded_freq_dict.items():
            context = ngram[:-1]
            context_frequencies[context] = context_frequencies.get(context, 0) + freq

        ngram_freq_dict = {}
        for ngram, freq in encoded_freq_dict.items():
            context_freq = context_frequencies.get(ngram[:-1], 0)
            if context_freq == 0:
                continue
            ngram_freq_dict[ngram] = freq / context_freq

        model = NGramLanguageModel(None, n_gram_size)
        model.set_n_grams(ngram_freq_dict)

        return model

        freq = self._content.get("freq")
        if not isinstance(freq, dict):
            return None

        ngram_counts = {}
        for n_gram in freq:
            cleaned_n_gram = ""
            for sym in n_gram:
                if sym.isspace():
                    cleaned_n_gram += self._eow_token
                elif sym.isalpha():
                    cleaned_n_gram += sym.lower()
                elif sym == self._eow_token:
                    cleaned_n_gram += sym
            if len(cleaned_n_gram) != n_gram_size:
                continue

            encoded = [self._text_processor.get_id(token) for token in cleaned_n_gram]
            if None not in encoded:
                ngram_counts[tuple(encoded)] = ngram_counts.get(tuple(encoded), 0) + freq[n_gram]

        context_counts = {}
        for n_gram, count in ngram_counts.items():
            context = n_gram[:-1]
            context_counts[context] = context_counts.get(context, 0) + count

        probabilities = {}
        for n_gram, count in ngram_counts.items():
            probabilities[n_gram] = count / context_counts[n_gram[:-1]]

        model = NGramLanguageModel(None, n_gram_size)
        model.set_n_grams(probabilities)
        return model
    def get_text_processor(self) -> TextProcessor:  # type: ignore[empty-body]
        """
        Get method for the processor created for the current JSON file.

        Returns:
            TextProcessor: processor created for the current JSON file.
        """
        return self._text_processor


class BackOffGenerator:
    """
    Language model for back-off based text generation.

    Attributes:
        _language_models (dict[int, NGramLanguageModel]): Language models for next token prediction
        _text_processor (TextProcessor): A TextProcessor instance to handle text processing
    """
    def __init__(
        self, language_models: tuple[NGramLanguageModel, ...], text_processor: TextProcessor
    ) -> None:
        """
        Initializes an instance of BackOffGenerator.

        Args:
            language_models (tuple[NGramLanguageModel, ...]):
                Language models to use for text generation
            text_processor (TextProcessor): A TextProcessor instance to handle text processing
        """
        self._language_models = {
            language_model.get_n_gram_size(): language_model
            for language_model in language_models
        }
        self._text_processor = text_processor

    def run(self, prompt: str, seq_len: int) -> str | None:
        """
        Generate sequence based on NGram language model and prompt provided.

        Args:
            prompt (str): Beginning of sequence
            seq_len (int): Number of tokens to generate

        Returns:
            str | None: Generated sequence

        In case of corrupt input arguments or methods used return None,
        None is returned
        """
        if not isinstance(seq_len, int) or seq_len <= 0:
            return None

        encoded_prompt = self._text_processor.encode(prompt)
        if encoded_prompt is None:
            return None

        sequence = list(encoded_prompt)
        for _ in range(seq_len):
            candidates = self._get_next_token(tuple(sequence))
            if candidates is None:
                return None
            if not candidates:
                break
            best_token_id = max((score, token_id) for token_id, score in candidates.items())[1]
            sequence.append(best_token_id)

        return self._text_processor.decode(tuple(sequence))

        if not all([prompt, seq_len > 0]):
            return None

        encoded_text = self._text_processor.encode(prompt)
        if not encoded_text:
            return None
        sequence = list(encoded_text)

        for _ in range(seq_len + 1):
            next_tokens = self._get_next_token(tuple(sequence))
            if next_tokens is None:
                return None
            if not next_tokens:
                break
            sorted_next_tokens = sorted(next_tokens.items(), key = lambda x: (-x[1], -x[0]))
            sequence.append(sorted_next_tokens[0][0])
        text = self._text_processor.decode(tuple(sequence))
        return text
    def _get_next_token(self, sequence_to_continue: tuple[int, ...]) -> dict[int, float] | None:
        """
        Retrieve next tokens for sequence continuation.

        Args:
            sequence_to_continue (tuple[int, ...]): Sequence to continue

        Returns:
            dict[int, float] | None: Next tokens for sequence continuation

        In case of corrupt input arguments return None.
        """
        if not isinstance(sequence_to_continue, tuple):
            return None

        for n_gram_size in sorted(self._language_models, reverse=True):
            model = self._language_models[n_gram_size]
            candidates = model.generate_next_token(sequence_to_continue)
            if candidates:
                return candidates

        return None
