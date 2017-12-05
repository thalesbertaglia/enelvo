'''Statistics and out-of-vocabulary words identification'''
import re
# Author: Thales Bertaglia <thalesbertaglia@gmail.com>


def identify_oov(lex, ignore_list, tokens):
    '''Returns a list containing all indexes of out-of-vocabulary words in ``text``.

    Args:
        lex (dict): The lexicon dictionary.
        ignore_list (dict): A dictionary containing words that are not correct but
                            might be improperly contained in ``lex``.
        tokens (list (str)): The preprocessed and sanitized text (i.e, no punctuation etc).

    Returns:
        list (int): Indexes of all out-of-vocabulary words in ``text``.
    '''
    oov = list()
    p = re.compile('(kk)+|(ha)+|(rs)+|(ks)+|(he)+|(hua)+|(hau)+|(hue)+')
    placeholders = ['username', 'url', 'number', 'emoji']
    for i in range(len(tokens)):
        t = tokens[i].lower()
        if str.isalpha(t) and not p.match(t) and not t in placeholders and len(t) < 15 and (t not in lex or t in ignore_list):
            oov.append(i)
    '''return [i for i in range(len(tokens)) if (tokens[i].lower() not in lex and str.isalpha(tokens[i]))
            or (tokens[i].lower() in ignore_list)]'''
    return oov
