from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.roles import register_local_role
import docutils.nodes
from docutils.utils import new_document

from sphinx.application import Sphinx
from sphinx.domains.std import StandardDomain
from sphinx.parsers import RSTParser

import pathlib


class SphinxFile:
    """Light wrapper of the docutils.nodes.document class for lazy parsing

    In an ideal world, this wrapper class would extend docutils.nodes.document directly,
    but that proved to be an annoying challenge.
    """

    def __init__(self, full_path, rel_path, settings, reporter, parser):
        # Set the docname variable
        settings.env.temp_data['docname'] = str(rel_path.with_suffix(''))

        # Report errors from the correct location
        reporter.source = str(rel_path)

        self.document = docutils.nodes.document(settings, reporter, source=full_path)
        self.document.note_source(full_path, -1)

        self.full_path = full_path
        self.rel_path = rel_path
        self.parser = parser

    def parse(self):
        # actual parsing
        self.parser.parse(open(self.full_path).read(), self.document)
        return self.document

    def __lt__(self, other):
        return self.rel_path < other.rel_path

    def __repr__(self):
        return str(self.rel_path)


def load_sphinx(src_path, conf_path):
    app = Sphinx(srcdir=src_path,
                 confdir=conf_path,
                 outdir='/tmp',
                 doctreedir='/tmp',
                 buildername='text',
                 status=None,           # Avoids printing status messages at startup
                 )
    parser = RSTParser()
    parser.config = app.config

    base_doc = new_document('base_doc')
    base_doc.settings.env = app.env

    # Default settings
    base_doc.settings.tab_width = 4
    base_doc.settings.pep_references = None
    base_doc.settings.rfc_references = None

    # Do not show warnings
    base_doc.reporter.report_level = 3

    # Unclear why I have to do these registrations manually
    for name, role in StandardDomain.roles.items():
        register_local_role(name, role)
    for name, directive in StandardDomain.directives.items():
        register_directive(name, directive)

    return base_doc.settings, base_doc.reporter, parser


def get_single_sphinx_file(filepath, conf_path):
    if not isinstance(filepath, pathlib.Path):
        filepath = pathlib.Path(filepath)
    if not isinstance(conf_path, pathlib.Path):
        conf_path = pathlib.Path(conf_path)

    settings, reporter, parser = load_sphinx(
        src_path=filepath.parent,
        conf_path=conf_path
    )
    rel_path = filepath.relative_to(filepath.parent)
    return SphinxFile(filepath, rel_path, settings, reporter, parser)


def get_sphinx_files(root_path, file_glob='*.rst'):
    if not isinstance(root_path, pathlib.Path):
        root_path = pathlib.Path(root_path)
    # For now, assume conf.py in root, and source in source
    src_path = root_path / 'source'
    settings, reporter, parser = load_sphinx(
        src_path=src_path,
        conf_path=root_path
    )

    # Iterate through all files, only yield .rst
    for path in sorted(src_path.rglob(file_glob), key=lambda p: str(p).lower()):
        rel_path = path.relative_to(src_path)
        yield SphinxFile(path, rel_path, settings, reporter, parser)
