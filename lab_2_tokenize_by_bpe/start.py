"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable, too-many-return-statements
from lab_2_tokenize_by_bpe.main import (
    calculate_bleu,
    collect_frequencies,
    decode,
    encode,
    get_vocabulary,
    load_vocabulary,
    train,
)


def main() -> None:
    """
    Launches an implementation
    """
    with open("lab_2_tokenize_by_bpe/assets/text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_raw.txt", "r", encoding="utf-8") as text_file:
        text_reference_translation = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/en_encoded.txt", "r", encoding="utf-8") as text_file:
        translation_encoded_raw = text_file.read().split()
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_2.txt", "r", encoding="utf-8") as file:
        secret_2 = file.read()
    with open ("lab_2_tokenize_by_bpe/assets/ru_raw.txt", "r", encoding="utf-8") as file:
        ru_raw = file.read()
    with open("lab_2_tokenize_by_bpe/assets/ru_encoded.txt", "r", encoding="utf-8") as file:
        ru_encoded = file.read().split()

    ru_encoded_int = [int(i) for i in ru_encoded]

    list_of_nums = [int(i) for i in secret_2.split()]

    result = None

    result = collect_frequencies(text, None, "</s>")

    merging_tokens = train(result, 100)
    if merging_tokens is None:
        return None

    dict_of_ident = get_vocabulary(merging_tokens, '<unk>')
    if dict_of_ident is None:
        return None

    decoded_text = decode(list_of_nums, dict_of_ident, "</s>")
    if decoded_text is None:
        return None

    print(decoded_text)

    vocab = load_vocabulary("lab_2_tokenize_by_bpe/assets/vocab.json")
    if vocab is None:
        return None

    encoded_text = encode(ru_raw, vocab, "\u2581", None, "<unk>")
    if encoded_text is None:
        return None

    if encoded_text[:20] == ru_encoded_int[:20]:
        print(encoded_text)

    translation_encoded_raw_int = [int(i) for i in translation_encoded_raw]

    decoded_text = decode(translation_encoded_raw_int, vocab, None)
    if decoded_text is None:
        return None

    decoded_text = decoded_text.replace("\u2581", " ")

    bleu = calculate_bleu(decoded_text, text_reference_translation)
    print(bleu)

    assert result, "Translation not working"
    return None


if __name__ == "__main__":
    main()
