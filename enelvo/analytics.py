'''Statistics and out-of-vocabulary words identification'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>


def identify_oov(lex, tokens):
    '''Returns a list containing all indexes of out-of-vocabulary words in ``text``.

    Args:
        lex (dict): The lexicon dictionary.
        tokens (list (str)): The preprocessed and sanitized text (i.e, no punctuation etc).

    Returns:
        list (int): Indexes of all out-of-vocabulary words in ``text``.
    '''
    return [i for i in range(len(tokens)) if tokens[i] not in lex]
