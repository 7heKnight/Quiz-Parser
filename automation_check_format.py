#! /usr/bin/python3
import re


class RegEx:
    S_CHARS = r'[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~ ]+'
    DOUBLE_SPACE = r'[ ]{2,}'
    A_AN = r'[aAsn() ]+ '
    NEW_LINE = r'[\r\n]+'
    THE = r'[tThe ]+ '


def remove_unwanted_char(text: str) -> str:
    text = re.sub(r'^' + RegEx.THE, '', text)
    text = re.sub(r'^' + RegEx.A_AN, '', text)
    text = re.sub(r'^' + RegEx.S_CHARS, '', text)
    text = re.sub(RegEx.NEW_LINE + RegEx.THE, '\n', text)
    text = re.sub(RegEx.NEW_LINE + RegEx.A_AN, '\n', text)
    text = re.sub(RegEx.NEW_LINE + RegEx.S_CHARS, '\n', text)
    text = re.sub(r'[ ?.]+\|', '|', text)
    text = re.sub(r'\([sS]e[^|]+\|', '|', text)
    text = re.sub(RegEx.S_CHARS + r'$', '', text)
    text = re.sub(RegEx.DOUBLE_SPACE, ' ', text)
    return text


def check_wrong_format(db: str):
    # Lines with a pipe but nothing after it on the same line (truncated key)
    pre = re.findall(r'[\r\n]+([^|\r\n]+\|)[\r\n]+', db)
    # Lines with no pipe at all (not a valid key)
    unknown_content = re.findall(r'[\r\n]+([^|\r\n]+)[\r\n]+', db)

    list_error = []
    errors_found = False

    if pre:
        print('   [-] Pre-QA (truncated — missing answer):')
        for key in pre:
            list_error.append(key)
            print(f'      [*]: {key}')
        errors_found = True

    if unknown_content:
        print('   [-] Unknown-QA (no pipe delimiter):')
        for key in unknown_content:
            list_error.append(key)
            print(f'      [*]: {key}')
        errors_found = True

    if not errors_found:
        print('[+] There is No key in wrong format.')

    return errors_found, list_error


def write_keys(list_keys: list, list_error: list):
    valid_keys = [k for k in list_keys if k and k not in list_error]
    with open('key.txt', 'w', encoding='utf8') as f:
        f.write('\n'.join(valid_keys))
    return len(valid_keys), 'key.txt'


if __name__ == '__main__':
    with open('key.txt', 'r', encoding='utf8') as f:
        open_file = f.read().lower()

    reformat_keys = remove_unwanted_char(open_file)
    print('[+] Removed unwanted character.')

    wrong_format, error_list = check_wrong_format(reformat_keys)

    reformat_keys = list(dict.fromkeys(reformat_keys.split('\n')))
    reformat_keys.sort(reverse=True)
    print('[+] Sorted lines in descending.')

    count, file_dir = write_keys(reformat_keys, error_list)
    print(f'[+] Wrote {count} keys into: {file_dir}')
    print('-----------------------------------------')
    print('Program executed successfully!')
