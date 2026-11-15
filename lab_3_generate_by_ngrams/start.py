"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from lab_3_generate_by_ngrams.main import (
    BackOffGenerator,
    BeamSearchTextGenerator,
    GreedyTextGenerator,
    NGramLanguageModel,
    NGramLanguageModelReader,
    TextProcessor,
    WordProcessor,
)


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(
        "./lab_3_generate_by_ngrams/assets/Harry_Potter.txt", "r", encoding="utf-8"
    ) as text_file:
        text = text_file.read()
    result = None

    processor = TextProcessor("_")

    encoded_text = processor.encode(text)
    if not isinstance(encoded_text, tuple):
        return None

    result = processor.decode(encoded_text)

    n_gramm = NGramLanguageModel(encoded_text, 7)
    mle = n_gramm.build()

    textgenerator = GreedyTextGenerator(n_gramm, processor)
    generated_text = textgenerator.run('Vernon', 51)

    print(generated_text)

    beam_search_generator = BeamSearchTextGenerator(n_gramm, processor, 3)

    generated_text_beam_search = beam_search_generator.run('Vernon', 56)
    print(generated_text_beam_search)

    reader = NGramLanguageModelReader("lab_3_generate_by_ngrams/assets/en_own.json", "_")

    models = []
    for i in range(2, 5):
        model = reader.load(i)
        if not model:
            return None
        models.append(model)


    back_off_generator = BackOffGenerator(tuple(models), processor)
    generated_back_off = back_off_generator.run("Vernon", 100)
    print(generated_back_off)

    result = generated_back_off

    word_processor = WordProcessor('<eos>')
    encoded_txt = word_processor.encode(text)

    model_with_bigram = NGramLanguageModel(encoded_txt, 2)
    model_with_bigram.build()
    model_with_trigram = NGramLanguageModel(encoded_txt, 3)
    model_with_trigram.build()
    model_with_tetragram = NGramLanguageModel(encoded_txt, 4)
    model_with_tetragram.build()

    word_greedy_generator = GreedyTextGenerator(model_with_tetragram, word_processor)
    greedy_word = word_greedy_generator.run("Harry looked at", 12)
    print(greedy_word)

    beam_search_word = BeamSearchTextGenerator(model_with_tetragram, word_processor, 3)
    beam_word = beam_search_word.run("Harry looked at", 12)
    print(beam_word)

    backoff_word = BackOffGenerator((model_with_bigram, model_with_trigram, model_with_tetragram),
                                                                                    word_processor)
    back_word = backoff_word.run("Harry looked at", 12)
    print(back_word)

    same_in_syms = textgenerator.run("Harry looked at", 60)
    print(same_in_syms)
    assert result
    return None


if __name__ == "__main__":
    main()
