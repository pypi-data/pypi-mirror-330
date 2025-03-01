from sphinx_tamer.sentence_scan import sphinx_sentence_scan
import pathlib


def test_project():
    data_folder = pathlib.Path('tests') / 'data'
    project_folder = data_folder / 'test_project'

    problems = sphinx_sentence_scan(project_folder)
    assert len(problems) == 2
