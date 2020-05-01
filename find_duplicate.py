#!/usr/bin/python

import hashlib
import os
import sys

file_list = {}
reverse_dict = {}


def hasher(saidfile, thumbprint):
    BLOCK_SIZE = 65536
    hash_function = getattr(hashlib, thumbprint.lower())()
    try:
        with open(saidfile, 'rb') as e:
            chunk = e.read(BLOCK_SIZE)
            while len(chunk) > 0:
                hash_function.update(chunk)
                chunk = e.read(BLOCK_SIZE)
    except IOError:
        print("{} : Cannot read file".format(saidfile))
        pass
    else:
        hash_result = hash_function.hexdigest()
        return hash_result, thumbprint


def chosen_dir(dir):
    try:
        os.path.exists(dir)
    except FileNotFoundError:
        print("directory not found")
    else:
        try:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    hash_result, thumbprint = hasher(
                        os.path.join(root, file), 'sha1')
                    file_list[(os.path.join(root, file))] = hash_result
        except TypeError:
            pass


def dict_rev(dic):
    for key, value in file_list.items():
        dic.setdefault(value, set()).add(key)


def find_duplicates(dir, revdir):
    chosen_dir(dir)
    dict_rev(revdir)


def Main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            find_duplicates(arg, reverse_dict)
        for keys, values in reverse_dict.items():
            if len(values) > 1:
                print("\x1b[1;32;40m{}\x1b[0m\n{}".format(
                      keys, "\n".join(values)))
    else:
        print("Usage: {} [dir_name]".format(sys.argv[0]))


if __name__ == '__main__':
    Main()
