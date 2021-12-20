import os, sys
import json


def main():
    input_dir = sys.argv[1]
    input_dir = os.path.abspath(input_dir)
    wav_root = input_dir.replace('ctm', 'wav')
    output_file = sys.argv[2]
    manifest = open(output_file, 'w', encoding='utf-8')
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.stm'):
                stm_file = os.path.join(root, file)
                wav_path = os.path.join(wav_root, file.replace('stm', 'wav'))
                with open(stm_file, 'r', encoding='utf-8') as s:
                    for line in s.readlines():
                        line_list = line.split('\t')
                        duration = float(line_list[4]) - float(line_list[3])
                        if len(line_list) == 6:
                            json_dict = {
                                'audio_filepath': wav_path,
                                'duration': duration,
                                'text': line_list[5].strip(),
                                'offset': float(line_list[3]),
                            }
                            manifest.write(json.dumps(json_dict, ensure_ascii=False)+'\n')
                        elif len(line_list) == 5:
                            json_dict = {
                                'audio_filepath': wav_path,
                                'duration': duration,
                                'text': '_',
                                'offset': float(line_list[3]),
                            }
                        else:
                            continue
                        

if __name__ == "__main__":
    main()
