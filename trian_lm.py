import os, sys
import subprocess
from typing import final



def main():
    # 新模型存放位置
    save_dir = sys.argv[1] # "/data1/asr-lm-data/english/New_data/command/frequent/command_all/v2
    save_dir = os.path.abspath(save_dir)
    version = os.path.basename(save_dir)
    final_arpa = os.path.join(save_dir, "final.arpa")
    final_bin = os.path.join(save_dir, "final.bin")
    target_text = "/data1/asr-lm-data/test_data/en_commands_faq.txt"
    srctxts = [
        # command text
        "/data1/asr-lm-data/english/New_data/command/frequent/App/App_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Clock/Clock_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Device/Device_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Music/Music_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Camera/Camera_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Communication/Communication_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/FM/FM_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Phone/Phone_templates_replace.txt",
        "/data1/asr-lm-data/english/New_data/command/frequent/Generic_templates.txt",
        # FAQ text
        "/data1/asr-lm-data/english/New_data/command/frequent/FAQ/FAQ_test_text.txt"
    ]

    intermediates = [
        # 训练音频的文本
        "/data1/asr-lm-data/english/New_data/command/audio_text/en_train.intermediate"
        # ted的文本
        "/data1/asr-lm-data/english/New_data/common/cantab-TEDLIUM/ted.intermediate"
    ]

    lmplz_path = "/home/liuanping/kenlm-master/build_zk/bin/lmplz"
    interpolate_path = "/home/liuanping/kenlm-master/build_zk/bin/interpolate"
    binary_path = "/home/liuanping/kenlm-master/build_zk/bin/build_binary"

    all_text = os.path.join(save_dir, version+".txt")
    command_arpa_path = os.path.join(save_dir, version+".arpa")
    intermediate_file = os.path.join(save_dir, version+".intermediate")
    txt_param = ' '.join(srctxts)
    subprocess.check_output(f"cat {txt_param} > {all_text}", shell=True)
    subprocess.check_output(
        f"{lmplz_path} -o 4 --text {all_text} --intermediate {intermediate_file} --arpa {command_arpa_path} --discount_fallback",
         shell=True
    )
    intermediates.append(intermediate_file)
    intermediate_param = ' '.join(intermediates)
    subprocess.check_output(
        f"{interpolate_path} -m {intermediate_param} -t {target_text} > {final_arpa}",
        shell=True
    )

    subprocess.check_output(
        f"{binary_path} trie -q 8 -b 7 -a 256 {final_arpa} {final_bin}",
        shell=True
    )

    print("done")


if __name__ == "__main__":
    main()