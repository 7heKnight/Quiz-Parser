#! /usr/bin/python3
# from os.path import realpath
import re


def remove_unwanted_char(list_qa: str):
    list_qa = re.sub(r'^[aAsn() ]+ |'
                     r'^[tThe ]+ |'
                     r'^[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~ ]+', '', list_qa)
    list_qa = re.sub(r'[\r\n]+[aAn() ]+ |'
                     r'[\r\n]+[tThe ]+ |'
                     r'[\r\n]+[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~ ]+', '\n', list_qa)
    list_qa = re.sub(r'[ ?.]+\|', '|', list_qa)
    list_qa = re.sub(r'\([sS]el[^|]+\|', '|', list_qa)
    list_qa = re.sub(r'[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~ ]+$', '', list_qa)
    list_qa = re.sub(r'[ ]{2,}', ' ', list_qa)
    return list_qa


def print_wrong(list_qa: list, list_error: list):
    for key in list_qa:
        list_error.append(key)
        print(f'      [*]: {key}')


def if_else_printer(message: str, list_qa: list, list_error):
    if len(list_qa) != 0:
        print(message)
        print_wrong(list_qa, list_error)
        return False, list_error
    return True, list_error


def check_wrong_format(db: str):
    # Finding wrong format
    pre = re.findall(r'[\r\n]+([^|\r\n]+\|)[\r\n]+', db)
    mid = re.findall(r'[\r\n|]+([^|\r\n]+?\|[^|\r\n]+\|[^|\r\n]+?)[|\r\n]+', db)  # Not working
    last = re.findall(r'[\r\n]+(\|[^|\r\n]+)[\r\n]+', db)  # Not working
    unknown_content = re.findall(r'[\r\n]+([^|\r\n]+)[\r\n]+', db)

    # Testing spot
    # print(len(pre))
    # print(len(mid))
    # print(len(last))
    # print(len(unknown_content))

    # Printing spot
    list_error = []
    checked_pre, list_error = if_else_printer('   [-] Pre-QA:', pre, list_error)
    checked_mid, list_error = if_else_printer('   [-] Mid-QA:', mid, list_error)
    checked_last, list_error = if_else_printer('   [-] Last-QA:', last, list_error)
    checked_unknown_content, list_error = if_else_printer('   [-] Unknown-QA:', unknown_content, list_error)
    if checked_pre and checked_mid and checked_last and checked_unknown_content:
        print('[+] There is No key in wrong format.')
        return False, list_error
    return True, list_error


def write_keys(list_keys: list, list_error: list):
    counter = 0
    with open('key.txt', 'w', encoding='utf8') as write_file:
        file_name = write_file.name
        for key in list_keys:
            if key and key not in list_error:
                counter += 1
                if key != list_keys[len(list_keys) - 1]:
                    write_file.write(f'{key}\n')
                else:
                    write_file.write(f'{key}')
                # write_file.write(f'{key}\n')
        write_file.close()
    return counter, file_name


if __name__ == '__main__':
    open_file = open('key.txt', 'r', encoding='utf8').read().lower()
    reformat_keys = remove_unwanted_char(open_file)
    print('[+] Removed unwanted character.')
    wrong_format, error_list = check_wrong_format(reformat_keys)
    reformat_keys = reformat_keys.split('\n')
    reformat_keys = list(dict.fromkeys(reformat_keys))
    reformat_keys.sort(reverse=True)
    print('[+] Sorted lines in descending.')
    if wrong_format:
        count, file_dir = write_keys(reformat_keys, error_list)
    else:
        count, file_dir = write_keys(reformat_keys, error_list)(f'{i}')
        #     write_file.close()
    print(f'[+] Wrote {count} keys into: {file_dir}')
    print('-----------------------------------------')
    print('Program executed successfully!')
