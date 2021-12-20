import os, sys
import json, subprocess
import librosa

def pre_one_pair(root, file):
    wav_path = os.path.join(root, file)
    json_path = os.path.join(root, file[:-3]+'json')
    txt_path = os.path.join(root, file[:-3]+'txt')
    if os.path.exists(json_path):
        json_file = open(json_path, 'r', encoding='utf-8')
        json_dict = json.load(json_file)
        json_file.close()
        duration = json_dict['end']
        text = json_dict['lines']
    elif os.path.exists(txt_path):
        txt_file = open(txt_path, 'r', encoding='utf-8')
        text = txt_file.read().strip()
        txt_file.close()
        wav_data, sample_rate = librosa.load(wav_path, sr=None)
        assert sample_rate == 16000
        duration = librosa.get_duration(wav_data, sr=sample_rate)
    else:
        print(wav_path, 'has no label')
        exit()
    return wav_path, duration, text


def main():
    data_dir = sys.argv[1]
    manifest_path = sys.argv[2]
    manifest_file = open(manifest_path, 'w', encoding='utf-8')
    data_dir = os.path.abspath(data_dir)

    line_dict = {}
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.wav'):
                wav_path_shell = os.path.join(root, file).replace(' ', '\ ')
                check_result = subprocess.check_output("file {}".format(wav_path_shell), shell=True)
                if 'RIFF' in check_result.decode():
                    wav_path, duration, text = pre_one_pair(root, file)
                    manifest_file.write(wav_path+'\t'+text+'\n')
    manifest_file.close()

if __name__ == "__main__":
    main()
