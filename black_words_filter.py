#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description       :Scripts for filtering black words.
@Date     :2022/08/26 14:36:20
@Author      :Lv Chuancheng
@version      :1.0
'''
import ahocorasick
import copy


def read_black_words(file_path: str):
    """Read the black words from the file.

    Args:
        file_path: The path of the black words file.

    Returns:
        A list of black words.
    """
    return [i.strip() for i in open(file_path,'r').readlines()]


def build_actree(word_list: list):
    """Build the actree from the list of words.

    Args:
        wordlist: The list of words.

    Returns:
        actree: The actree build with the words.
    """
    actree = ahocorasick.Automaton()
    for index, word in enumerate(word_list):
        actree.add_word(word, (index, word))
    actree.make_automaton()
    return actree


def filter_black_words(actree, content: str, replace_char: str = '*'):
    """Filter the black words in the content.

    Args:
        actree: The actree of the black words.
        content: The content need to be filtered.
        replace_char: The char used to replace the black words.

    Returns:
        filtered_content: The filtered content.
        black_words: The black words.
    """
    filtered_content = copy.deepcopy(content)
    black_words = []
    for match in actree.iter(content):
        filtered_content = filtered_content.replace(
            match[1][1], replace_char * len(match[1][1]))
        black_words.append(match[1][1])
    return filtered_content, black_words


if __name__ == '__main__':
    word_list = read_black_words('./black_words')
    actree = build_actree(word_list=word_list)
    while True:
        content = input("Enter(q for quit) :")
        if content == "q":
            break
        filtered_content, black_words = filter_black_words(actree, content)
        print("Filtered content:", filtered_content)
        print("Black words:", black_words)
