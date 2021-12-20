import os, sys, gc
from functools import partial
from tqdm import tqdm

def is_in_28alpha(ch):
    """ 判断字符是否在28个字符中[" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                   "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "'"]
    """
    ch_ord = ord(ch)
    if (ch_ord >=97 and ch_ord <= 122) or \
        ch_ord == 32 or ch_ord == 39:
        return True
    else:
        return False


def chunked_file_reader(file, block_size=1024 * 8):
    """生成器函数：分块读取文件内容，使用 iter 函数
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    for chunk in iter(partial(file.read, block_size), ''):
        yield chunk


def main():
    input_file_path = sys.argv[1]
    chunk_size = 1<<32   # 4GB
    chars = set()
    
    input_file_list = input_file_path.split(',')
    for input_file in input_file_list:
        with open(input_file, 'r', encoding="utf-8") as f:
            for text in tqdm(chunked_file_reader(f, chunk_size)):
                cur_set = set(text)
                chars = chars.union(cur_set)
                del text, cur_set
                gc.collect()

    char_list = list(chars)
    char_list.sort()
    for char in char_list:
        print(char, '\t', ord(char))
    print("all_chars: ", len(char_list), "\n", char_list)


if __name__ == "__main__":
    main()