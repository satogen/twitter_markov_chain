#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from glob import iglob
import re

import MeCab
import markovify


def load_from_file(files_pattern):
    """read and merge files which matches given file pattern, prepare for parsing and return it.
    """

    # read text
    text = ""
    for path in iglob(files_pattern):
        with open(path, 'r') as f:
            text += f.read().strip()

    # delete some symbols
    unwanted_chars = ['\r', '\u3000', '-', '｜']
    for uc in unwanted_chars:
        text = text.replace(uc, '')

    # delete aozora bunko notations
    unwanted_patterns = [re.compile(r'《.*》'), re.compile(r'［＃.*］')]
    for up in unwanted_patterns:
        text = re.sub(up, '', text)

    return text


def split_for_markovify(text):
    """split text to sentences by newline, and split sentence to words by space.
    """
    # separate words using mecab
    mecab = MeCab.Tagger()
    splitted_text = ""

    # these chars might break markovify
    # https://github.com/jsvine/markovify/issues/84
    breaking_chars = [
        '(',
        ')',
        '[',
        ']',
        '"',
        "'",
    ]

    # split whole text to sentences by newline, and split sentence to words by space.
    for line in text.split():
        mp = mecab.parseToNode(line)
        while mp:
            try:
                if mp.surface not in breaking_chars:
                    splitted_text += mp.surface    # skip if node is markovify breaking char
                if mp.surface != '。' and mp.surface != '、':
                    splitted_text += ' '    # split words by space
                if mp.surface == '。':
                    splitted_text += '\n'    # reresent sentence by newline
            except UnicodeDecodeError as e:
                # sometimes error occurs
                print(line)
            finally:
                mp = mp.next

    return splitted_text


def main():
    # load text
    rampo_text = load_from_file('text_w.txt')
    # print()
    # split text to learnable form
    splitted_text = split_for_markovify(rampo_text)

    # print(splitted_text)
    # learn model from text.
    text_model = markovify.NewlineText(splitted_text, state_size=3)

    # ... and generate from model.
    for i in range(30):
        try:
            sentence = text_model.make_sentence()
            print(''.join(sentence.split()))    # need to concatenate space-splitted text
        except:
            sentence = text_model.make_sentence()
            print(sentence)
    # save learned data 
    with open('learned_data.json', 'w') as f:
        f.write(text_model.to_json())

    start_text_model = text_model.make_sentence_with_start(beginning="バンコク")
    print(start_text_model)
    # later, if you want to reuse learned data...
    """
    with open('learned_data.json') as f:
        text_model = markovify.NewlineText.from_json(f.read())
    """


if __name__ == '__main__':
    main()
