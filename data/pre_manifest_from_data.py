import json
import os, sys
import json
import librosa


def main():
    data_dir = sys.argv[1]
    manifest_path = sys.argv[2]

    scp = open(os.path.join(data_dir, 'wav.scp'), 'r', encoding='utf-8')
    text = open(os.path.join(data_dir, 'text'), 'r', encoding='utf-8')
    manifest = open(manifest_path, 'w', encoding='utf-8')

    m = {}
    for line in scp:
        uttid, wav_path = line.strip().split('\t')
        m[uttid] = {}
        m[uttid]["audio_filepath"] = wav_path
    for line in text:
        if '\t' in line:
            uttid, wav_txt = line.strip().split('\t')
        else:
            uttid, wav_txt = line.strip().split()[0], ' '.join(line.strip().split()[1:-1])
        m[uttid]["text"] = wav_txt
    
    if os.path.exists(os.path.join(data_dir, 'utt2dur')):
        with open(os.path.join(data_dir, 'utt2dur'), 'r', encoding='utf-8') as f:
            for line in f:
                if '\t' in line:
                    uttid, duration = line.strip().split('\t')
                else:
                    uttid, duration = line.strip().split()
                m[uttid]["duration"] = float(duration)               
    else:
        for uttid in m.keys():
            audio, sr = librosa.load(m[uttid]["audio_filepath"])
            duration = librosa.get_duration(audio, sr)
            m[uttid]["duration"] = duration   

    for uttid in m.keys():
        manifest.write(json.dumps(m[uttid], ensure_ascii=False)+'\n')
    manifest.close()


if __name__ == "__main__":
    main()