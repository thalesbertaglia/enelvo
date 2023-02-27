"""Preprocessing methods."""
from .tokenizer import Tokenizer
import emoji
import string
import os.path

basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, ".."))
# Author: Thales Bertaglia <thalesbertaglia@gmail.com>


def new_readable_tokenizer():
    """Creates a tokenizer that does not replace entities (hashtags, numbers etc).

    Returns:
        obj: The tokenizer.
    """
    return Tokenizer(
        usernames=False,
        urls=False,
        hashtags=False,
        phonenumbers=False,
        times=False,
        numbers=False,
    )


def tokenize(text, tokenizer=None, as_string=False):
    """Tokenizes ``text``using ``tokenizer``.
    Returns tokens as a list, if ``as_string`` = False or as a string otherwise.

    Args:
        tokenizer (obj): Instance of Tokenizer to be used.
        text (str): Text to be tokenized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of tokens if ``as_string`` = False.
        str: Tokenized text if ``as_string`` = True.
    """
    if tokenizer is None:
        tokenizer = Tokenizer()
    tokenized = tokenizer.tokenize(text)
    tokenized = [t.lower() for t in tokenized]
    return tokenized if not as_string else " ".join(tokenized)


def sanitize(text, as_string=False):
    """Additional preprocessing steps. Removes punctuation, emojis and emoticons.

    Args:
        text (str): Text to be tokenized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of tokens if ``as_string`` = False.
        str: Tokenized text if ``as_string`` = True.
    """
    if isinstance(text, list):
        text = " ".join(text)
    translator = str.maketrans("", "", string.punctuation)
    emoticons = [
        w.strip()
        for w in open(
            filepath + "/preprocessing/tokenizer/lexicons/emoticons.txt",
            encoding="utf-8",
        ).readlines()
    ]
    tokens = text.translate(translator).split(" ")
    clean = [
        w.strip()
        for w in tokens
        if w not in emoticons and emoji.emoji_count(w) == 0 and len(w) != 0
    ]
    return clean if not as_string else " ".join(clean)


def capitalize_initials(tokens, as_string=False):
    """Capitalizes the initial word of each sentence in ``tokens``.

    Args:
        tokens (list (str)): Tokenized text to be capitalized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of capitalized tokens if ``as_string`` = False.
        str: Tokenized capitalized text if ``as_string`` = True.
    """
    tokens[0] = tokens[0][0].upper() + tokens[0][1:]

    for i in range(1, len(tokens)):
        if tokens[i - 1] in ".!?":
            tokens[i] = tokens[i][0].upper() + tokens[i][1:]

    return tokens if not as_string else " ".join(tokens)


def capitalize_proper_nouns(lex, tokens, as_string=False):
    """Capitalizes all proper nouns in ``tokens``.

    Args:
        lex (dict): Lexicon dictionary containing the list of proper nouns.
        tokens (list (str)): Tokenized text to be capitalized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of tokens if ``as_string`` = False.
        str: Tokenized text if ``as_string`` = True.
    """
    for i in range(len(tokens)):
        if tokens[i] in lex:
            tokens[i] = tokens[i][0].upper() + tokens[i][1:]

    return tokens if not as_string else " ".join(tokens)


def capitalize_acronyms(lex, tokens, as_string=False):
    """Capitalizes all acronyms in ``tokens``.

    Args:
        lex (dict): Lexicon dictionary containing the list of acronyms.
        tokens (list (str)): Tokenized text to be capitalized.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of tokens if ``as_string`` = False.
        str: Tokenized text if ``as_string`` = True.
    """
    for i in range(len(tokens)):
        if tokens[i] in lex:
            tokens[i] = tokens[i].upper()

    return tokens if not as_string else " ".join(tokens)


def preprocess(
    text,
    tokenizer=None,
    pn_lex=None,
    ac_lex=None,
    capitalize_inis=True,
    capitalize_pns=False,
    capitalize_acs=False,
    do_sanitize=False,
    as_string=False,
):
    """Applies all preprocessing steps.

    Args:
        pn_lex (dict): Lexicon dictionary containing the list of proper nouns.
        ac_lex (dict): Lexicon dictionary containing the list of proper acronyms.
        tokenizer (obj): Instance of Tokenizer to be used.
        text (str): Text to be tokenized.
        capitalize_inis (boolean): Whether to capitalize initials or not.
        capitalize_pns (boolean): Whether to capitalize proper nouns or not.
        capitalize_acs (boolean): Whether to capitalize acronyms or not.
        do_sanitize (boolean): Whether to sanitize the texr or not.
        as_string (boolean): Whether to return the tokens as a list (False) or a string (True).

    Returns:
        list (str): List of preprocessed tokens if ``as_string`` = False.
        str: Preprocessed text if ``as_string`` = True.
    """
    if tokenizer is None:
        tokenizer = Tokenizer()
    tokens = tokenize(text, tokenizer)

    if capitalize_inis:
        tokens = capitalize_initials(tokens)

    if capitalize_pns:
        tokens = capitalize_proper_nouns(pn_lex, tokens)

    if capitalize_acs:
        tokens = capitalize_acronyms(ac_lex, tokens)

    if do_sanitize:
        tokens = sanitize(tokens)

    return tokens if not as_string else " ".join(tokens)
