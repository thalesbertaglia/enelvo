#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A simple example showing how to integrate Enelvo to your code, using it as a library.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

# normaliser contains the Normaliser class
from enelvo import normaliser


def main():
    # Let's use this sentence as example
    sentence = 'hj eh q dia vc sbe?'
    # Creates a normaliser object with default attributes.
    norm = normaliser.Normaliser()
    # Now, let's normalise the original sentence
    norm_sentence = norm.normalise(sentence)
    # Simple! Let's see the result
    print(norm_sentence)
    # We can change any attributes we want
    norm.capitalize_inis = True
    # Let's see the result
    print(norm.normalise(sentence))
    # That's all!

if __name__ == '__main__': main()
