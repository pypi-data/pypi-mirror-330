from sphinx_tamer.sentences import split_into_sentences
import pathlib


def test_from_files():
    data_folder = pathlib.Path('tests') / 'data'
    for n in range(1, 3):
        path = data_folder / f'{n}.txt'
        for line in open(path).readlines():
            line = line.strip()
            sentences = split_into_sentences(line)
            assert len(sentences) == n, sentences
