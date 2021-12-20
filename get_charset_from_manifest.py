import os, sys, json


def main():
    manifest_file = sys.argv[1]
    manifest = open(manifest_file, 'r', encoding='utf-8')
    lines = manifest.readlines()
    charset = set()
    for line in lines:
        line_dict = json.loads(line)
        charset = charset.union(set(line_dict["text"]))
    print("char number: ", len(charset), '\n')
    print("char set: ", charset, '\n')
    for char in charset:
        print(char, '\t', ord(char))

if __name__ == "__main__":
    main()

