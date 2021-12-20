import os, sys, json
import librosa
import multiprocessing as mlp
from tqdm import tqdm

def get_wav_duration(wav_path):
    try:
        audio, sr = librosa.load(wav_path, None)
    except:
        print(wav_path, " can't open!")
        return 0
    if sr != 16000:
        print(wav_path, " have worry samplerate")
        exit()
    duration = librosa.get_duration(audio, sr)
    return duration


def main():
    wav_dir = sys.argv[1]
    tasks = []
    pool = mlp.Pool(32)

    duration_all = 0
    for root, dirs, files in os.walk(wav_dir):
        for file in files:
            if file.lower().endswith('.wav'):
                wav_path = os.path.join(root, file)
                tasks.append(pool.apply_async(get_wav_duration, (wav_path,)))

    for i in tqdm(range(len(tasks))):
        duration_all += tasks[i].get()
    print("duration(s): ", "%.2f" % duration_all)
    print("duration(h): ", "%.2f" % (duration_all/3600))

if __name__ == "__main__":
    main()

