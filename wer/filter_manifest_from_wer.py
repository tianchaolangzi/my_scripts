import os, sys, json


def main():
    manifest = sys.argv[1]
    wer_file = sys.argv[2]
    out_manifest = sys.argv[3]

    fout = open(out_manifest, 'w', encoding='utf8')
    wav_set = set()
    with open(wer_file, 'r', encoding='utf8') as fin:
        lines = fin.readlines()
        for i in range(0, len(lines), 7):
            if not lines[i+2].startswith("WER:"):
                break
            utt_id = lines[i+1].split(':')[1].strip()
            wav_set.add(utt_id)
    print(f"{wer_file} has {len(wav_set)} utts")
    lines = open(manifest, 'r', encoding='utf8').readlines()
    out_num = 0
    for line in lines:
        wav_id = json.loads(line)["audio_filepath"].split('/')[-1][:-4]
        if wav_id in wav_set:
            out_num += 1
            fout.write(line)
    fout.close()
    print(f"write {out_num} cases")


if __name__ == "__main__":
    main()