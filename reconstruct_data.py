import sys, os
import shutil


def main():
    src_dirs = sys.argv[1]
    dst_dir = sys.argv[2]
    pre_str = sys.argv[3]
    start_num = int(sys.argv[4])
    dir_list = src_dirs.split(',')
    num = start_num

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for dir_ in dir_list:
        abs_dir = os.path.abspath(dir_)
        for root, dirs, files in os.walk(abs_dir):
            for file in files:
                if file.endswith('.wav'):
                    wav_path = os.path.join(root, file)
                    txt_path = wav_path.replace('.wav', '.txt')
                    if not os.path.exists(txt_path):
                        continue
                    new_name = pre_str+"_%09d" % num
                    new_wav_path = os.path.join(dst_dir, new_name+'.wav')
                    new_txt_path = os.path.join(dst_dir, new_name+'.txt')
                    #shutil.copy(wav_path, new_wav_path)
                    #shutil.copy(txt_path, new_txt_path)
                    shutil.move(wav_path, new_wav_path)
                    shutil.move(txt_path, new_txt_path)
                    num += 1
    
if __name__ == "__main__":
    main()