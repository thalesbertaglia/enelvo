#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# tweetokenize: Regular expression based tokenizer for Twitter
# Copyright: (c) 2013, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import unittest
from tweetokenize.tokenizer import Tokenizer


class TokenizeTests(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer(lowercase=True)

    def test_general_1(self):
        self.tokenizer.normalize = 2
        msg = ('omg wow &#x3c; &#x26; &#x3e; &#62;.&#60; &gt;.&lt; :):)'
               'i CANT believe thatttt haha lol!!1')
        tks = ['omg', 'wow', '<', '&', '>', '>.<', '>.<', ':)', ':)',
               'i', 'CANT', 'believe', 'thatt', 'haha', 'lol', '!', '!', '1']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_general_2(self):
        msg = "i'm wanting to jump up and down but wouldn't if i couldn't.."
        tks = ["i'm", 'wanting', 'to', 'jump', 'up', 'and', 'down',
               'but', "wouldn't", 'if', 'i', "couldn't", '...']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_urls_1(self):
        msg = ("hey bro chec'k out http://shitstorm.com its fucking sick")
        tks = ['hey', 'bro', "chec'k", 'out', 'URL', 'its', 'fucking', 'sick']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_urls_2(self):
        msg = ('also see this crazy stuff https://shitstorm.com')
        tks = ['also', 'see', 'this', 'crazy', 'stuff', 'URL']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_urls_3(self):
        msg = 'hiiiii rayj.com/ihititfirst and other google.com http://hobo.net'
        tks = ['hiii', 'URL', 'and', 'other', 'URL', 'URL']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_usernames_1(self):
        msg = ('@justinbeiber yo man!! ! i love you in a totally '
               'straight way <3:p:D')
        tks = ['USERNAME', 'yo', 'man', '!', '!', '!',
               'i', 'love', 'you', 'in', 'a', 'totally', 'straight', 'way',
               '<3', ':p', ':D']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_usernames_2(self):
        msg = '@heyheymango: what did you SAYYY??? or did you just..  NotHING?'
        tks = ['USERNAME', ':', 'what', 'did', 'you', 'SAYYY', '?',
               '?', '?', 'or', 'did', 'you', 'just', '...', 'nothing', '?']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_numbers_1(self):
        self.tokenizer.numbers = None
        msg = ('i have this much money -2.42 in my bank acct.,friend! but you '
               'have mucho +88e44 and its about 1000% more than $400.')
        tks = ['i', 'have', 'this', 'much', 'money', '-2.42', 'in',
               'my', 'bank', 'acct', '.', ',', 'friend', '!', 'but', 'you',
               'have', 'mucho', '+88e44', 'and', 'its', 'about', '1000%',
               'more', 'than', '$400', '.']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_numbers_2(self):
        msg = ('i have this much money -2.42 in my bank acct.,friend! but you '
               'have mucho +88e44 and its about 1000% more than $400.')
        tks = ['i', 'have', 'this', 'much', 'money', 'NUMBER', 'in',
               'my', 'bank', 'acct', '.', ',', 'friend', '!', 'but', 'you',
               'have', 'mucho', 'NUMBER', 'and', 'its', 'about', 'NUMBER',
               'more', 'than', 'NUMBER', '.']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_numbers_3(self):
        self.tokenizer.lowercase = False  # keep cases the same everywhere
        msg = ('I JUST want To Test FRACTIONZZZ 22432.41414/ 55894385e-341 also'
               ' lowercase etc.etc.etc. hope that last part doesn\'t parse as a url '
               'i would be kinda sad PANda!zsss..... .. . .... 4/5 5.1/4.0e0 3.14 -2')
        tks = ['I', 'JUST', 'want', 'To', 'Test', 'FRACTIONZZZ',
               'NUMBER', 'also', 'lowercase', 'etc', '.', 'etc', '.', 'etc',
               '.', 'hope', 'that', 'last', 'part', "doesn't", 'parse', 'as',
               'a', 'url', 'i', 'would', 'be', 'kinda', 'sad', 'PANda', '!',
               'zsss', '...', '...', '.', '...', 'NUMBER', 'NUMBER', 'NUMBER',
               'NUMBER']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_time_1(self):
        msg = 'is the time now 12:14pm? or is it like 2:42AM??'
        tks = ['is', 'the', 'time', 'now', 'TIME', '?', 'or', 'is',
               'it', 'like', 'TIME', '?', '?']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_time_2(self):
        msg = 'new time is 2:42:09 PM!!'
        tks = ['new', 'time', 'is', 'TIME', '!', '!']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_phonenumber_1(self):
        msg = ('my number is 18002432242 and 241.413.5584 also 1-242-156-6724'
               ' and (958)555-4875 or (999) 415 5542 is 422-5555 a 131-121-1441')
        tks = ['my', 'number', 'is', 'PHONENUMBER', 'and', 'PHONENUMBER',
               'also', 'PHONENUMBER', 'and', 'PHONENUMBER', 'or', 'PHONENUMBER',
               'is', 'PHONENUMBER', 'a', 'PHONENUMBER']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_phonenumber_2(self):
        msg = 'numbers with extension: (201)-340-4915 x112 or 1 800.341.1311x99'
        tks = ['numbers', 'with', 'extension', ':', 'PHONENUMBER', 'or',
               'PHONENUMBER']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_quotes_1(self):
        self.tokenizer.ignorequotes = True
        msg = 'this is just a tweet with "someone said something funny" lol'
        tks = ['this', 'is', 'just', 'a', 'tweet', 'with', 'lol']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_quotes_2(self):
        self.tokenizer.ignorequotes = False
        msg = 'this is just a tweet with "someone said something funny" lol'
        tks = ['this', 'is', 'just', 'a', 'tweet', 'with', '"', 'someone',
               'said', 'something', 'funny', '"', 'lol']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_quotes_3(self):
        self.tokenizer.ignorequotes = True
        msg = ('some stuff but he said “yea i know its crazy”other '
               'stuff...!!! ')
        tks = ['some', 'stuff', 'but', 'he', 'said', 'other', 'stuff',
               '...', '!', '!', '!']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_quotes_4(self):
        self.tokenizer.ignorequotes = True
        msg = ('some stuff but he said &ldquo;yea i know its crazy&rdquo;other '
               'stuff...!!! ')
        tks = ['some', 'stuff', 'but', 'he', 'said', 'other', 'stuff',
               '...', '!', '!', '!']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_quotes_5(self):
        self.tokenizer.ignorequotes = False
        msg = 'heyy buddyyyyy boy \'do you the lady\'s kitty like that??\''
        tks = ['heyy', 'buddyyy', 'boy', "'", 'do', 'you', 'the',
               "lady's", 'kitty', 'like', 'that', '?', '?', "'"]
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_hashtags_1(self):
        msg = 'omg i love#dog#cat#food#other#things#so#fucking#much!!!11LOLOLOL'
        tks = ['omg', 'i', 'love', '#dog', '#cat', '#food', '#other',
               '#things', '#so', '#fucking', '#much', '!', '!', '!', '11LOLOLOL']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_hashtags_2(self):
        self.tokenizer.hashtags = 'HASHTAG'
        msg = 'omg i love#dog#cat#food#other#things#so#fucking#much!!!11LOLOLOL'
        tks = ['omg', 'i', 'love', 'HASHTAG', 'HASHTAG', 'HASHTAG',
               'HASHTAG', 'HASHTAG', 'HASHTAG', 'HASHTAG', 'HASHTAG', '!', '!', '!',
               '11LOLOLOL']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_emoticons_1(self):
        msg = 'heyyyyyy:):):(>.<<v.vwhats up man LOL T.T tomcat.tomcat :$;).!!!'
        tks = ['heyyy', ':)', ':)', ':(', '>.<', '<', 'v.v', 'whats',
               'up', 'man', 'LOL', 'T.T', 'tomcat', '.', 'tomcat', ':$',
               ';)', '.', '!', '!', '!']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_removefeatures_1(self):
        self.tokenizer.usernames = ""  # dont' want any usernames to show
        msg = ('hey @arnold @nickelodeon #90s#ilove90s#allthat#amandashow'
               '@rocko http://en.wikipedia.org/wiki/The_Angry_Beavers ^.^>>><<<^.^')
        tks = ['hey', '#90s', '#ilove90s', '#allthat', '#amandashow',
               'URL', '^.^', '>', '>', '>', '<', '<', '<', '^.^']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_removefeatures_2(self):
        self.tokenizer.usernames = ""  # dont' want any usernames to show
        self.tokenizer.hashtags = ""  # or hashtags
        msg = ('hey @arnold @nickelodeon #90s#ilove90s#allthat#amandashow'
               '@rocko http://en.wikipedia.org/wiki/The_Angry_Beavers ^.^>>><<<^.^')
        tks = ['hey', 'URL', '^.^', '>', '>', '>', '<', '<', '<',
               '^.^']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_removefeatures_3(self):
        self.tokenizer.usernames = False  # keep usernames
        self.tokenizer.urls = ""         # URLs should be removed
        self.tokenizer.hashtags = "$$$"  # hashtags should be $$$
        msg = ('hey @arnold @nickelodeon #90s#ilove90s#allthat#amandashow'
               '@rocko http://en.wikipedia.org/wiki/The_Angry_Beavers ^.^>>><<<^.^')
        tks = ['hey', '@arnold', '@nickelodeon', '$$$', '$$$', '$$$',
               '$$$', '@rocko', '^.^', '>', '>', '>', '<', '<', '<', '^.^']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_emoji_1(self):
        msg = ('hey mate!:):3.....@and🇨🇳ONE+ BRO#love😘😵💚💛💜💙  '
               '💋😂😂LOLLLL.')
        tks = ['hey', 'mate', '!', ':)', ':3', '...',
               'USERNAME', '\U0001f1e8\U0001f1f3', 'ONE', '+', 'BRO', '#love',
               '\U0001f618', '\U0001f635', '\U0001f49a', '\U0001f49b',
               '\U0001f49c', '\U0001f499', '\U0001f48b', '\U0001f602',
               '\U0001f602', 'LOLLL', '.']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_emoji_2(self):
        msg = ('hey mate!:):3.....@andONE+🇬🇧  BRO#love😘😵💚💛💜💙  '
               '💋😂😂LOLLLL.')
        tks = ['hey', 'mate', '!', ':)', ':3', '...',
               'USERNAME', '+', '\U0001f1ec\U0001f1e7', 'BRO', '#love', '😘',
               '😵', '\U0001f49a', '\U0001f49b', '\U0001f49c',
               '\U0001f499', '💋', '\U0001f602', '\U0001f602',
               'LOLLL', '.']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_emoji_3(self):
        msg = ('🚀=)</3O_O:$D:<:-@\xf0\x9f\x98\xb7🔥💩💅 outdated:💽 ancient:💾 '
               '#getwiththecloud:💻 and it looks like 💭')
        tks = ['\U0001f680', '=)', '</3', 'O_O', ':$', 'D:<', ':-@',
               '\U0001f637', '\U0001f525', '\U0001f4a9', '\U0001f485',
               'outdated', ':', '\U0001f4bd', 'ancient', ':',
               '\U0001f4be', '#getwiththecloud',
               ':', '\U0001f4bb', 'and', 'it', 'looks', 'like', '\U0001f4ad']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_error_1(self):
        msg = []
        with self.assertRaises(TypeError):
            self.tokenizer.tokenize(msg)

    def test_error_2(self):
        msg = lambda x: x
        with self.assertRaises(TypeError):
            self.tokenizer.tokenize(msg)

    def test_actual_tweets_1(self):
        "Number as part of name"
        msg = '@LoganTillman not 2pac and floyd mayweather'
        tks = ['USERNAME', 'not', '2pac', 'and', 'floyd', 'mayweather']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_actual_tweets_2(self):
        "Colon no space in hashtag"
        msg = '#MentionSomeoneYoureGladYouMet: @LarryWorld_Wide of course.'
        tks = ['#MentionSomeoneYoureGladYouMet', ':', 'USERNAME', 'of',
               'course', '.']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

    def test_stopwords_1(self):
        self.tokenizer.ignorestopwords = True
        msg = 'i like myself and my so not much and our something he:)'
        tks = ['like', 'much', 'something', ':)']
        self.assertEqual(self.tokenizer.tokenize(msg), tks)

if __name__ == "__main__":
    unittest.main()
