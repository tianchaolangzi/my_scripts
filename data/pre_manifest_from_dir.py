import os, sys
import json
import librosa
import multiprocessing as mlp
from tqdm import tqdm

def get_one(txt_file, wav_path):
    texts = open(txt_file, 'r', encoding='utf-8').read().strip()
    lines = texts.split('\n')
    if len(lines) == 1:
        text = lines[0].strip()
        audio, sr = librosa.load(wav_path, sr=None)
        if sr != 16000:
            print(f"{wav_path} samplerate is {sr}, skip!")
            return ''
        duration = librosa.get_duration(audio, sr)
        json_dict = {
            'audio_filepath': wav_path,
            'duration': duration,
            'text': text,
        }
        return json.dumps(json_dict, ensure_ascii=False)+'\n'
    else:
        print(f"{txt_file} has more than one line, skip!")
        return ''


def main():
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    manifest = open(output_file, 'w', encoding='utf-8')
    input_dir = os.path.abspath(input_dir)
    tasks = []
    pool = mlp.Pool(32)
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                txt_file = os.path.join(root, file)
                wav_path = txt_file.replace('.txt', '.wav')
                if not os.path.exists(wav_path):
                    continue
                tasks.append(pool.apply_async(get_one, (txt_file, wav_path)))

    for i in tqdm(range(len(tasks))):
        manifest.write(tasks[i].get())
    manifest.close()


if __name__ == "__main__":
    main()
