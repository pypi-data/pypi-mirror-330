import docutils.nodes
import sphinx.addnodes
NONPARSING_TYPES = (
    docutils.nodes.literal,
    docutils.nodes.title_reference,
    sphinx.addnodes.pending_xref
)


class PartialNode:
    def __init__(self, src, text, initial_src=''):
        self.src = src
        self.text = text
        self.initial_src = initial_src

    def __repr__(self):
        return self.initial_src + self.src


class TextLine:
    def __init__(self, nodes, path, line_num, tail_src=''):
        self.nodes = nodes
        self.path = path
        self.line_num = line_num
        self.tail_src = tail_src

    def get_text(self):
        return ''.join(n.text for n in self.nodes)

    def get_source(self):
        return ''.join(n.initial_src + n.src for n in self.nodes) + self.tail_src

    def get_location(self):
        return f'{self.path}:{self.line_num}'

    def get_source_sentences(self, text_sentences):
        # This state machine is more complex than I'd like
        # and future-me will curse its opaque nature.
        src_sentences = []

        running_text_i = 0
        current_text_i = 0
        node_i = 0
        node_s_i = 0
        current_src = ''
        remaining_text_len = len(self.nodes[node_i].text)

        for text in text_sentences:
            running_text_i += len(text)

            while current_text_i < running_text_i or node_i < len(self.nodes):
                node = self.nodes[node_i]
                node_s = str(node)[node_s_i:]

                diff = running_text_i - current_text_i
                if diff > remaining_text_len:
                    current_src += node_s
                    node_s_i = 0
                    node_i += 1
                    current_text_i += remaining_text_len
                    remaining_text_len = len(self.nodes[node_i].text)
                else:
                    chunk_length = len(node.initial_src) + diff
                    back_count = node_s[:chunk_length].count('\\')
                    if back_count:
                        chunk_length += back_count
                    portion = node_s[:chunk_length]
                    current_src += portion
                    src_sentences.append(current_src)
                    current_src = ''

                    node_s_i += chunk_length
                    current_text_i += chunk_length
                    remaining_text_len -= chunk_length
                    break

        if self.tail_src:
            src_sentences[-1] += self.tail_src

        return src_sentences

    def __repr__(self):
        return self.get_source()


class ParagraphParser:
    def __init__(self, paragraph):
        self.lines = []
        self.source = paragraph.source
        self.line_num = paragraph.line
        self.raw_src = paragraph.rawsource
        self.current = []

        for child in paragraph.children:
            self.process_node(child)

        if self.current:
            self.lines.append(TextLine(self.current, self.source, self.line_num, self.raw_src))

    def consume_src(self, src):
        if src in self.raw_src:
            # Usually can handle the quick way if nothing needs escaping
            src_index = self.raw_src.index(src)
            initial_src = self.raw_src[:src_index]
            self.raw_src = self.raw_src[src_index + len(src):]
            return initial_src, src

        # If there is some escaping that needs to be done,
        # grab the initial portion, then match char by char
        src_index = self.raw_src.index(src[0])
        initial_src = self.raw_src[:src_index]

        text_i = 0
        assert len(self.raw_src[src_index:]) > len(src)
        actual_src = ''
        while text_i < len(src):
            if self.raw_src[src_index] == src[text_i]:
                actual_src += src[text_i]
                src_index += 1
                text_i += 1
            elif self.raw_src[src_index] == '\\':
                actual_src += '\\'
                src_index += 1
            else:
                raise RuntimeError('Error in the source parsing. Problem with escaping?')  # pragma: no cover

        self.raw_src = self.raw_src[src_index:]
        return initial_src, actual_src

    def process_node(self, node):
        if isinstance(node, docutils.nodes.Text):
            self.process_text_node(node)
        elif isinstance(node, NONPARSING_TYPES):
            initial_src, src = self.consume_src(node.rawsource)
            self.current.append(PartialNode(src, '', initial_src))
        else:
            for child in node.children:
                self.process_node(child)

    def process_text_node(self, node):
        node_text = node.astext()
        initial_src, node_src = self.consume_src(node_text)
        if '\n' not in node_text:
            self.current.append(PartialNode(node_src, node_text, initial_src))
            return

        text_start_i = 0
        src_start_i = 0

        while '\n' in node_text[text_start_i:]:
            text_end_i = node_text.index('\n', text_start_i)
            src_end_i = node_src.index('\n', src_start_i)

            partial_src = node_src[src_start_i:src_end_i]
            partial_text = node_text[text_start_i:text_end_i]
            self.current.append(PartialNode(partial_src, partial_text, initial_src))
            initial_src = ''
            text_start_i = text_end_i + 1
            src_start_i = src_end_i + 1

            self.lines.append(TextLine(self.current, self.source, self.line_num))
            self.current = []
            self.line_num += 1

        if initial_src or text_start_i < len(node_text) or src_start_i < len(node_src):
            partial_src = node_src[src_start_i:]
            partial_text = node_text[text_start_i:]
            self.current.append(PartialNode(partial_src, partial_text, initial_src))

    def __iter__(self):
        yield from self.lines


def get_paragraphs(obj):
    """Return all paragraphs that are part of this object EXCEPT those part of system_messages"""
    # This is easier to yield from than a NodeVisitor

    if isinstance(obj, docutils.nodes.paragraph):
        yield obj
    elif not isinstance(obj, docutils.nodes.system_message):
        for child in obj.children:
            yield from get_paragraphs(child)


def get_lines(obj):
    """Yield all of the TextLine objects from this object."""
    if isinstance(obj, docutils.nodes.paragraph):
        yield from ParagraphParser(obj)
    elif isinstance(obj, docutils.nodes.document):
        for paragraph in get_paragraphs(obj):
            yield from get_lines(paragraph)
    else:
        raise RuntimeError(f'Unable to get lines from object of type {type(obj)}')  # pragma: no cover
