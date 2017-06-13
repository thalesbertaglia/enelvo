'''Preprocessing methods.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>


def tokenize(tokenizer, text, as_string=False):
    '''Tokenizes ``text``using ``tokenizer``.
    Returns tokens as a list, if ``as_string`` = False or as a string otherwise.

    Args:
        tokenizer (obj): Instance of Tokenizer to be used.
        text (str): Text to be tokenized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of tokens if ``as_string`` = False.
        str: Tokenized text if ``as_string`` = True.
    '''
    tokenized = tokenizer.tokenize(text)
    return tokenized if not as_string else ' '.join(tokenized)


def capitalize_initials(tokens, as_string=False):
    '''Capitalizes the initial word of each sentence in ``tokens``.

    Args:
        tokens (list (str)): Tokenized text to be capitalized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of capitalized tokens if ``as_string`` = False.
        str: Tokenized capitalized text if ``as_string`` = True.
    '''
    tokens[0] = tokens[0][0].upper() + tokens[0][1:]

    for i in range(1, len(tokens)):
        if tokens[i-1] == '.': tokens[i] = tokens[i][0].upper() + tokens[i][1:]

    return tokens if not as_string else ' '.join(tokens)

def capitalize_proper_nouns(lex, tokens, as_string=False):
    '''Capitalizes all proper nouns in ``tokens``.

    Args:
        lex (dict): Lexicon dictionary containing the list of proper nouns.
        tokens (list (str)): Tokenized text to be capitalized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of tokens if ``as_string`` = False.
        str: Tokenized text if ``as_string`` = True.
    '''
    for i in range(len(tokens)):
        if tokens[i] in lex: tokens[i] = tokens[i][0].upper() + tokens[i][1:]

    return tokens if not as_string else ' '.join(tokens)


def preprocess(tokenizer, text, lex=None, capitalize_inis=True, capitalize_pns=False, as_string=False):
    '''Applies all preprocessing steps.

    Args:
        lex (dict): Lexicon dictionary containing the list of proper nouns.
        tokenizer (obj): Instance of Tokenizer to be used.
        text (str): Text to be tokenized.
        capitalize_inis (boolean): Whether to capitalize initials or not.
        capitalize_pns (boolean): Whether to capitalize proper nouns or not.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of preprocessed tokens if ``as_string`` = False.
        str: Preprocessed text if ``as_string`` = True.
    '''
    tokens = tokenize(tokenizer, text)

    if capitalize_inis: tokens = capitalize_initials(tokens)

    if capitalize_pns: tokens = capitalize_proper_nouns(lex, tokens)

    return tokens if not as_string else ' '.join(tokens)
