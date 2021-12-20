import sys


def main():
    wer_file = sys.argv[1]
    strong_label_file = wer_file+'_strong_label'
    weak_label_file = wer_file+'_weak_label'

    count1 = count2 = 0

    with open(wer_file, 'r', encoding='utf8') as fin:
        with open(strong_label_file, 'w', encoding='utf8') as fout1:
            with open(weak_label_file, 'w', encoding='utf8') as fout2:
                lines = fin.readlines()
                for i in range(0, len(lines), 6):
                    # print(lines[i+2].split(' '))
                    if not lines[i+2].startswith("WER:"):
                        break
                    _, wer, _, _, _, _, delete, insert = lines[i+2].split(' ')
                    wer = float(wer)
                    del_num = int(delete.split('=')[1])
                    ins_num = int(insert.split('=')[1])

                    if del_num == 0 and ins_num == 0 and wer <= 40:
                        fout1.write(''.join(lines[i:i+7]))
                        count1 += 1
                    else:
                        fout2.write(''.join(lines[i:i+7]))
                        count2 += 1
    print("strong label utt numbers: ", count1)
    print("weak label utt numbers: ", count2)

if __name__ == "__main__":
    main()
