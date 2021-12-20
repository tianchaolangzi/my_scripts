import os, sys, json


def main():
    manifest_file = sys.argv[1]
    manifest = open(manifest_file, 'r', encoding='utf-8')
    lines = manifest.readlines()
    duration_all = 0
    for line in lines:
        line_dict = json.loads(line)
        duration_all += float(line_dict["duration"])
    print("duration(s): ", "%.2f" % duration_all)
    print("duration(h): ", "%.2f" % (duration_all/3600))

if __name__ == "__main__":
    main()

