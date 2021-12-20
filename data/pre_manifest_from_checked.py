import os, sys
import json
import multiprocessing as mlp
from tqdm import tqdm


def get_one(json_file, wav_path):
    re = ""
    with open(json_file, 'r', encoding='utf-8-sig') as s:   
        for line in s.readlines():
            json_dict = json.loads(line)
            try:
                duration = float(float(json_dict['end']) - float(json_dict['begin']))
                if duration < 0.05:
                    print(wav_path, " too short")
                    continue
            except:
                print(json_file, " has problem")
            if isinstance(json_dict["lines"], list):
                if len(json_dict["lines"]) == 1:
                    text = json_dict["lines"][0]
                else:
                    print(f"{json_file} have problem")
                    continue
            elif isinstance(json_dict["lines"], str):
                text = json_dict["lines"]#.decode('unicode-escape')
            offset = float(json_dict['begin'])
            manifest_dict = {
                "audio_filepath": wav_path,
                "duration": duration,
                "text": text,
                "offset": offset,
            }
            re += (json.dumps(manifest_dict, ensure_ascii=False)+'\n')
    return re



def main():
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    manifest = open(output_file, 'w', encoding='utf-8')
    input_dir = os.path.abspath(input_dir)
    tasks = []
    pool = mlp.Pool(32)

    
    print("preparing tasks")
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                wav_path = json_file.replace('.json', '.wav')
                if not os.path.exists(wav_path):
                    continue
                tasks.append(pool.apply_async(get_one, (json_file, wav_path)))

    print("doing tasks")
    for i in tqdm(range(len(tasks))):
        manifest.write(tasks[i].get())      
    manifest.close()


if __name__ == "__main__":
    main()
