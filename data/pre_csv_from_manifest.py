import os, sys
import json


def main():
    manifest = sys.argv[1]
    csv = sys.argv[2]

    with open(manifest, 'r', encoding='utf8') as fin:
        with open(csv, 'w', encoding='utf8') as fout:
            for line in fin:
                line_dict = json.loads(line.strip())
                fout.write(line_dict["audio_filepath"] + '\t'+ line_dict["text"]+'\n')


if __name__ == "__main__":
    main()