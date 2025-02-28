from sphinx_tamer import get_sphinx_files, get_lines
from sphinx_tamer.sentences import split_into_sentences, register_extra_pattern
import pathlib
import yaml


def is_ignorable(rel_path_s, prefixes):
    for prefix in prefixes:
        if rel_path_s.startswith(prefix):
            return True


def sphinx_sentence_scan(root_folder, ignorable_prefixes=[]):
    config_path = root_folder / '.sphinx_tamer.yaml'
    if config_path.exists():
        config = yaml.safe_load(open(config_path))
        scan_config = config.get('sentence_scan', {})
        for pattern_text in scan_config.get('extra_patterns', []):
            register_extra_pattern(pattern_text)
        ignorable_prefixes += scan_config.get('ignorable_prefixes', [])

    problems = []
    for sphinx_file in get_sphinx_files(root_folder):
        if is_ignorable(str(sphinx_file.rel_path), ignorable_prefixes):
            continue
        for line in get_lines(sphinx_file.parse()):
            sentences = split_into_sentences(line.get_text())
            if len(sentences) <= 1:
                continue

            problems.append({
                'location': line.get_location(),
                'path': line.path,
                'line_num': line.line_num,
                'sentences': line.get_source_sentences(sentences),
            })
    return problems


def main():  # pragma: no cover
    import argparse
    import click

    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=pathlib.Path)
    parser.add_argument('-i', '--ignorable-prefixes', nargs='+', default=[])
    args = parser.parse_args()

    problems = sphinx_sentence_scan(args.folder, args.ignorable_prefixes)
    for problem in problems:
        flag = True
        click.secho(f'{len(problem["sentences"])} sentences found at {problem["location"]} ', bg='yellow', fg='black')
        for sentence in problem['sentences']:
            click.secho(f'\t{sentence.strip()}', fg='bright_green' if flag else 'green')
            flag = not flag
        click.secho('')

    if problems:
        click.secho(f'{len(problems)} Total Errors!', fg='red')
    else:
        click.secho('No errors!', fg='blue')
