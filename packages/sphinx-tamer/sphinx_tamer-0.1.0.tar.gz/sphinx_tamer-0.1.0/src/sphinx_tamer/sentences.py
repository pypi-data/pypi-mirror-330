import re

# Derived from https://stackoverflow.com/a/31505798
DOT = '•'
QUESTION = '✇'
EXCLAM = '‼'
SP_LOOKUP = {
    '.': DOT,
    '?': QUESTION,
    '!': EXCLAM,
}
STOP = '¶'

# Classes and patterns
ALPHABETIC = r'([A-Za-z])'
DIGITS = '([0-9])'
DOT_GROUP = r'([\.•])'

LETTER_DOT_LETTER = re.compile(ALPHABETIC + r'(\.)' + ALPHABETIC)
DIGITS_DOT_DIGITS = re.compile(DIGITS + r'(\.)' + DIGITS)
SINGLE_LETTER = re.compile(r'(\s[A-Z])(\.)(\s)')

# Common abbreviations, followed by a dot, and then either whitespace, a comma or an end paren
COMMON_ABBREVIATIONS = re.compile(r'(Mr|St|Mrs|Ms|Dr|etc|vol|vs|cf)(\.)([\s,)])')
MULTIPLE_DOT_EXPRESSIONS = [
    ['e', 'g'],
    ['i', 'e'],
    ['Ph', 'D'],
    ['a', 'k', 'a'],
    ['w', 'r', 't']
]
DOT_PAREN = re.compile(r'\.( \()')


EXTRA_PATTERNS = []


def register_extra_pattern(pattern_text):
    EXTRA_PATTERNS.append(re.compile(pattern_text))


register_extra_pattern('et al.')


def iterative_pattern_replace(text, pattern):
    index = 0
    m = pattern.search(text)
    while m:
        whole_match = m.group(0)
        replacement = str(whole_match)
        for old, replace in SP_LOOKUP.items():
            replacement = replacement.replace(old, replace)
        index += m.span()[1]
        text = text.replace(whole_match, replacement)
        m = pattern.search(text[index:])
    return text


def split_into_sentences(text):
    """
    Split the text into sentences.
    Assumes text does not contain the special characters: •✇‼¶
    :param text: text to be split into sentences
    :type text: str
    :return: list of sentences
    :rtype: list[str]
    """

    # Replace all ellipses
    text = iterative_pattern_replace(text, re.compile(DOT_GROUP + DOT_GROUP + DOT_GROUP))

    # Using patterns with three groups, convert nonbreaking punctuation to special characters
    for pattern in [LETTER_DOT_LETTER, DIGITS_DOT_DIGITS, SINGLE_LETTER, COMMON_ABBREVIATIONS]:
        m = pattern.search(text)
        while m:
            whole_match = m.group(0)
            before, punctuation, after = m.groups()
            replacement = SP_LOOKUP[punctuation]
            text = text.replace(whole_match, before + replacement + after)
            m = pattern.search(text)

    for multiple_dot_expr in MULTIPLE_DOT_EXPRESSIONS:
        joiner = DOT_GROUP + r'\s*'
        pattern = re.compile(joiner.join(multiple_dot_expr) + DOT_GROUP + r'[\s,:]', re.IGNORECASE)
        text = iterative_pattern_replace(text, pattern)

    text = iterative_pattern_replace(text, re.compile(r'[!\.?][")][!\.?:]?$'))

    for pattern in EXTRA_PATTERNS:
        text = iterative_pattern_replace(text, pattern)

    # Convert breaking punctuation to include STOP character
    # and convert special characters back to normal
    for stopper, replacement in SP_LOOKUP.items():
        text = text.replace(stopper, stopper + STOP)
        text = text.replace(replacement, stopper)

    sentences = text.split(STOP)

    return list(filter(None, sentences))
