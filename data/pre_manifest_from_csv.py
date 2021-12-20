import os, sys
import json
import librosa


def main():
    csv = sys.argv[1]
    manifest = sys.argv[2]

    with open(csv, 'r', encoding='utf8') as fin:
        with open(manifest, 'w', encoding='utf8') as fout:
            for line in fin:
                wav_path, text = line.strip().split('\t')
                wav_data, sr = librosa.load(wav_path, None)
                if sr != 16000:
                    print(f"{wav_path} samplerate is {sr} not 16k")
                duration = librosa.get_duration(wav_data, sr)
                line_dict = {
                    "audio_filepath": wav_path,
                    "duration": duration,
                    "text": text
                }
                fout.write(json.dumps(line_dict, ensure_ascii=False)+'\n')
    
    print("done")


if __name__ == "__main__":
    main()