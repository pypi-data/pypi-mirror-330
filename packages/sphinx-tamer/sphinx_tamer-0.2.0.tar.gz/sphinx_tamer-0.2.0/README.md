# ![sphinx_tamer](Logo.png)
Python library for easy parsing of Sphinx documentation

## Installation
[![PyPI version](https://badge.fury.io/py/sphinx_tamer.svg)](https://badge.fury.io/py/sphinx_tamer)

    sudo pip3 install sphinx_tamer

![CI Status](https://github.com/DLu/sphinx_tamer/actions/workflows/main.yaml/badge.svg)


## Wrapper for Sphinx
In an ideal world, manually parsing a Sphinx reStructuredText document might look something like

```python
from sphinx.parsers import RSTParser
from sphinx.util.docutils import new_document

filepath = 'path/to/Documentation.rst'

parser = RSTParser()
document = new_document(filepath)
parser.parse(open(filepath).read(), document)
```

However, it ends up being much more complicated than that.
 * You need to manually load in some of the default settings like `tab_width`
 * You need to read your local Sphinx configuration (``conf.py``)
 * And more...! (including a bunch of edge case stuff that I don't understand yet)

All of this is handled in [`sphinx_wrapper.py`](src/sphinx_tamer/sphinx_wrapper.py). Instead, your code could look like this:

```python
from sphinx_tamer import get_single_sphinx_file

filepath = 'path/to/Documentation.rst'
conf_path = 'path/to/folder_with_conf.py'

sphinx_file = get_single_sphinx_file(filepath, conf_path)
document = sphinx_file.parse()

```

The library also handles iterating through all the files.
```python
from sphinx_tamer import get_sphinx_files

for sphinx_file in get_sphinx_files('path/to/root_sphinx_folder'):
    document = sphinx_file.parse()
```

## Checking The Text
The default parser in Sphinx breaks down documents into nodes of various types, including [paragraphs](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#paragraphs) which are parsed into plain text and [formatted bits](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#inline-markup) and [links](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#hyperlink-targets).
However, these pieces are NOT broken up on a line-by-line basis.

The [`get_lines` function](src/sphinx_tamer/text.py) reparses the output of the standard parser into `TextLine` objects. Not only do these objects allow you to get the raw source of the line (including formatting), it also allows you to get just the "text-y" bits, i.e. remove the formatting markup and targets of links. This makes it much easier to do text-based operations like splitting the text into sentences and checking spelling of the real words. The `TextLine` also has the attributes `path` and `line_num`, which can be formatted together with `get_location()`.

```python
from sphinx_tamer import get_sphinx_files, get_lines

for sphinx_file in get_sphinx_files('path/to/root_sphinx_folder'):
    document = sphinx_file.parse()
    for line in get_lines(document):
        print(line.get_location())
        print(f'Source: {line.get_source()}')
        print(f'Text  : {line.get_text()}')
```

## Sentence Splitting
Rather than relying on a weighty full-text-parsing library, we have a [home-grown sentence parsing library](src/sphinx_tamer/sentences.py).

The core function, `split_into_sentences` will at its core, split the given string up by any of these three sentence ending characters: `.` (a period), `!` (an exclamation point) or `?` (a question mark).

Example:
```python
from sphinx_tamer.sentences import split_into_sentences
split_into_sentences('Oh yeah! Can you picture that? Groovy.')
# Result: ['Oh yeah!', ' Can you picture that?', ' Groovy.']
```

However, it will also recognize a bunch of patterns that do not constitute sentence-breaks.
```python
split_into_sentences('Dr. Teeth does not have a Ph. D. unfortunately.')
# Result: ['Dr. Teeth does not have a Ph. D. unfortunately.']
```

## Sphinx Sentence Scanner
The code in [sentence_scan.py](src/sphinx_tamer/sentence_scan.py) provides different ways to combine the Sphinx parsing abilities with the sentence splitting, so as to check if each line has at most one sentence on it.

 * You can use the function `sphinx_sentence_scan()` to gather all of the instances of multi-sentence lines.
 * You can run the executable `sphinx_sentence_scan` with an argument of the root Sphinx folder to print out the results of the above call.

The goal is to eventually integrate `sphinx_sentence_scan()` into either a `pre-commit` hook or GitHub action or both.

You can also customize two aspects of the behavior using a config file located at the root Sphinx folder, named `.sphinx_tamer.yaml`. In the namespace `senence_scan` you can add
 * `extra_patterns` - a list of strings containing sentence ending characters that should not be considered sentence-breaks.
 * `ignorable_prefixes` - a list of strings specifying prefixes to the relative paths of files that should NOT be parsed.

Ideally, there would have been an easy way to in-line mark lines to ignore, but inline comments in RST are odd.
