#!/usr/bin/python
import argparse
import hashlib

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
        print("Requires a file only")
    else:
        hash_result = hash_function.hexdigest()
        return hash_result, thumbprint


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Return the hash of given file")
    parser.add_argument("thumbprint",
                        help="Enter the desired hash function:\n"
                        "md5, sha1, sha224, sha256, sha384, sha512")
    parser.add_argument("-c", "--compare",
                        help="compare a provided hash object "
                        "with the file hash")

    args = parser.parse_args()
    hash_result, thumbprint = hasher(args.file, args.thumbprint)
    if args.compare:
        if args.compare == hash_result:
            print("Integrity OK")
        else:
            print("Integrity Compromised!")
    else:
        print("{}: {}\n".format(thumbprint.upper(), hash_result))


if __name__ == '__main__':
    Main()
