"""
Generation by NGrams starter
"""

# pylint:disable=too-many-locals, unused-import, unused-variable
from main import TextProcessor


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

    result = processor.decode(encoded_text)

    assert result


if __name__ == "__main__":
    main()
