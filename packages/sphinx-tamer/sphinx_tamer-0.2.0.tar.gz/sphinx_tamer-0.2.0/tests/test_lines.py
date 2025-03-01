from sphinx_tamer import get_single_sphinx_file, get_sphinx_files, get_lines
from sphinx_tamer.sentences import split_into_sentences
import pathlib


def test_project():
    data_folder = pathlib.Path('tests') / 'data'
    project_folder = data_folder / 'test_project'
    rst_filepath = project_folder / 'source' / 'Documentation.rst'

    LINES = [
        (4, 'This is a normal sentence. This sentence is on the same line.'),
        (5, 'This sentence is on the next line.'),
        (9, 'This is also a normal sentence.'),
        (10, 'This one has some ``literals`` mixed in for ``fun``. This one has some *italic* text and **bold** text.'),
        (14, '*This one* starts with formatting **and then has more**'),
        (16, 'This line has a raw asterisk \\* in it.'),
        (17, 'This bit has a raw asterisk \\* and another \\* and then some ``literals``. It\'s also fun.'),
        (22, 'Here is a sentence with a `link <https://www.python.org/>`_.'),
    ]

    SENTENCES = [
        'This is a normal sentence.',
        ' This sentence is on the same line.',
        'This sentence is on the next line.',
        'This is also a normal sentence.',
        'This one has some ``literals`` mixed in for ``fun``.',
        ' This one has some *italic* text and **bold** text.',
        '*This one* starts with formatting **and then has more**',
        'This line has a raw asterisk \\* in it.',
        'This bit has a raw asterisk \\* and another \\* and then some ``literals``.',
        ' It\'s also fun.',
        'Here is a sentence with a `link <https://www.python.org/>`_.'
    ]

    sphinx_file = get_single_sphinx_file(str(rst_filepath), str(project_folder))
    assert str(sphinx_file) == rst_filepath.name
    document = sphinx_file.parse()
    for line in get_lines(document):
        line_num, next_line = LINES.pop(0)
        assert str(line) == next_line
        assert line.get_location() == f'{rst_filepath}:{line_num}'
        sentences = split_into_sentences(line.get_text())
        for sentence in line.get_source_sentences(sentences):
            next_sentence = SENTENCES.pop(0)
            assert sentence == next_sentence


def test_iteration():
    data_folder = pathlib.Path('tests') / 'data'
    project_folder = data_folder / 'test_project'
    sphinx_files = sorted(get_sphinx_files(str(project_folder)))
    assert len(sphinx_files) == 2
    assert str(sphinx_files[0]) == 'Documentation.rst'
