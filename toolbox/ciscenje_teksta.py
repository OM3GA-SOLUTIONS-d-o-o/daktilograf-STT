# -*- coding: utf-8 -*-

import string
import collections
import re

import num2words

#
#   Paterni brojeva
#
int_pattern = re.compile(r'[0-9]+')
float_pattern = re.compile(r'[0-9]+[,\.][0-9]+')

#
#   Dozvoljeni karakteri a-zA-Z'čćšđž
#
allowed = list(string.ascii_lowercase)
allowed.append(' ')
allowed.extend(list('čćšđž'))

#
#   Zamjena karaktera
#
replacer = {
    'àáâãåāăąǟǡǻȁȃȧ': 'a',
    'æǣǽ': 'a',
    'çĉċ': 'c',
    'ď': 'd',
    'èéêëēĕėęěȅȇȩε': 'e',
    'ĝğġģǥǧǵ': 'g',
    'ĥħȟ': 'h',
    'ìíîïĩīĭįıȉȋ': 'i',
    'ĵǰ': 'j',
    'ķĸǩǩκ': 'k',
    'ĺļľŀł': 'l',
    'м': 'm',
    'ñńņňŉŋǹ': 'n',
    'òóôõøōŏőǫǭǿȍȏðοœ': 'o',
    'ŕŗřȑȓ': 'r',
    'śŝşș': 's',
    'ţťŧț': 't',
    'ùúûũūŭůűųȕȗ': 'u',
    'ŵ': 'w',
    'ýÿŷ': 'y',
    'źżȥ': 'z',
    'ß': 'b',
    '-­': ' '
}

#
#   Dodatna pravila za zamjenu
#

special_replacers = {
    ' $ ': 'dolar',
    ' £ ': 'funta',
    'm³': 'kubni metar',
    'km²': 'kilometar kvadratni',
    'm²': 'metar kvadratni',
    'm2': 'metara kvadratnih'
    
}

replacements = {}
replacements.update(special_replacers)

for all, replacement in replacer.items():
    for to_replace in all:
        replacements[to_replace] = replacement


#
#   Alati
#

def replace_symbols(word):
    """ Primjeni sve zamjene karaktera/riječi za datu riječ. """
    result = word

    for to_replace, replacement in replacements.items():
        result = result.replace(to_replace, replacement)

    return result


def remove_symbols(word):
    """ Ukloni sve simbole koji nisu dozvoljeni. """
    result = word
    bad_characters = []

    for c in result:
        if c not in allowed:
            bad_characters.append(c)

    for c in bad_characters:
        result = result.replace(c, '')

    return result


def word_to_num(word):
    """ Zamjeni sve brojeve s njihovim nazivima. """
    result = word

    match = float_pattern.search(result)

    while match is not None:
        num_word = num2words.num2words(float(match.group().replace(',', '.')), lang='sr').lower()
        before = result[:match.start()]
        after = result[match.end():]
        result = ' '.join([before, num_word, after])
        match = float_pattern.search(result)

    match = int_pattern.search(result)

    while match is not None:
        num_word = num2words.num2words(int(match.group()), lang='sr')
        before = result[:match.start()]
        after = result[match.end():]
        result = ' '.join([before, num_word, after])
        match = int_pattern.search(result)

    return result


def get_bad_character(text):
    """ Vrati sve karaktere koji nisu dozvoljeni u tekt. """
    bad_characters = set()

    for c in text:
        if c not in allowed:
            bad_characters.add(c)

    return bad_characters


def clean_word(word):
    """
    Očisti datu riječ.

    1. brojevi u riječi
    2. zamjeniti karaktere/pravila
    3. obrisati nedozvoljene simbole
    """
    word = word.lower()
    word = word_to_num(word)
    word = replace_symbols(word)
    word = remove_symbols(word)

    bad_chars = get_bad_character(word)

    if len(bad_chars) > 0:
        print('Bad characters in "{}"'.format(word))
        print('--> {}'.format(', '.join(bad_chars)))

    return word


def clean_sentence(sentence):
    """
    Očisti datu rečenicu.

    1. razdvojiti riječi razmakom
    2. brojevi u riječi
    3. zamjeniti karaktere/pravila
    4. obrisati nedozvoljene simbole
    4. spojiti razmacima
    """
    words = sentence.strip().split(' ')
    cleaned_words = []

    for word in words:
        cleaned_word = clean_word(word)
        cleaned_words.append(cleaned_word)

    return ' '.join(cleaned_words)