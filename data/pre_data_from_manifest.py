import os, sys
import json


def main():
    manifest_path = sys.argv[1]
    data_dir = sys.argv[2]

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    scp_path = os.path.join(data_dir, 'wav.scp')
    text_path = os.path.join(data_dir, 'text')
    utt2spk_path = os.path.join(data_dir, 'utt2spk')
    scp = open(scp_path, 'w', encoding='utf-8')
    text = open(text_path, 'w', encoding='utf-8')
    utt2spk = open(utt2spk_path, 'w', encoding='utf-8')

    #count = 0
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_dict = json.loads(line.strip())
            wav_path = line_dict["audio_filepath"]
            uttid = wav_path.split('/')[-1][:-4]
            spkid = uttid
            txt = line_dict["text"]
            scp.write(uttid+'\t'+wav_path+'\n')
            text.write(uttid+'\t'+txt+'\n')
            utt2spk.write(uttid+'\t'+spkid+'\n')
            #count += 1
    scp.close()
    text.close()
    utt2spk.close()

if __name__ == "__main__":
    main()