"""
BPE Tokenizer starter
"""

# pylint:disable=too-many-locals, unused-variable
from main import (
    collect_frequencies,
    decode,
    get_vocabulary,
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
        translation_encoded_raw = text_file.read()
    with open("lab_2_tokenize_by_bpe/assets/secrets/secret_5.txt", "r", encoding="utf-8") as file:
        secret_5 = file.read()

    list_of_nums = [
        int(i) for i in secret_5.split()
    ]

    result = None

    result = collect_frequencies(text, None, "</s>")

    merging_tokens = train(result, 100)

    dict_of_ident = get_vocabulary(merging_tokens, '<unk>')

    decoded_text = decode(list_of_nums, dict_of_ident, "</s>")

    print(decoded_text)

    assert result, "Translation not working"

    return


if __name__ == "__main__":
    main()
