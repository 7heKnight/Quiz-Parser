import time
import sys
import re
import os

SPLITQUESTION = '"~~"'
SPLITQA = '"**"'

BANNER = r'''
===============================================================================
  ___        _          ____                            |
 / _ \ _   _(_)____    |  _ \ __ _ _ __ ___  ___ _ __   |
| | | | | | | |_  /____| |_) / _` | '__/ __|/ _ \ '__|  |
| |_| | |_| | |/ /_____|  __/ (_| | |  \__ \  __/ |     |
 \__\_\\__,_|_/___|    |_|   \__,_|_|  |___/\___|_|     |   Version: 1
                                                        |   Made by 7heKnight
===============================================================================
'''

HELP = fr'''
---------------------------------------------------------------------------------------------

[*] Usage: python {sys.argv[0]} <Option number> <Question and answer in raw>
    - Option 1: Parsing the question and answer which is have the format like flashcard. It will pass the key if duplicated.
    - Option 2: Parsing the question have the multi-choice and answer is only character. It will pass the key if duplicated.
    - Option 3: Swaping the position of question and answer.
    - Option 4: Checking and removing key if each key in wrong form.

---------------------------------------------------------------------------------------------

* Option 1 and 2 will append to key.txt. Option 3 will not create any but it will overriden the file. Option 4 will create the similar file with extension (*.log)

*** Export note: Custom on the left must be {SPLITQUESTION} and the right custom is {SPLITQA}.

'''


def remove_unwanted(sub):
    sub = re.sub(r'[(cC ]{1,}hoose 1 answer[) ]{0,1}', '', sub)
    sub = re.sub(r'[_]+', '', sub)
    return sub


def read_file(file_path):
    existing_keys = set()
    try:
        with open('key.txt', 'r', encoding='UTF-8') as f:
            content = f.read()
        content = re.sub('[*]{3,99}', '', content)
        content = re.sub('[~]{3,99}', '', content)
        for line in content.strip().split('\n'):
            line = line.strip()
            if line:
                existing_keys.add(line)
    except FileNotFoundError:
        pass

    raw_list = []
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            raw_list = f.read().split(SPLITQA)
        if raw_list:
            raw_list.pop()
    except IOError:
        print('[-] Error while opening files.')
    return existing_keys, raw_list


def parse_question_type1(existing_keys, raw_list):
    final_list = []
    for item in raw_list:
        cleaned = item.replace('\n', ' ').replace('  ', ' ')
        parts = cleaned.split(SPLITQUESTION)
        if len(parts) < 2:
            continue
        question = parts[0]
        question = remove_unwanted(question)
        question = re.sub(r'^[# ]{1,2}', '', question)
        question = re.sub(r'^[tT]/[fF][ ]{0,2}', '', question)
        question = re.sub(r'^[_]+[ ]?', '', question)
        question = re.sub(r'^[0-9]{1,3}[.) ]{1,3}', '', question)
        question = re.sub(r'^[a-z]{1,2}=[0-9]{1,3}[ ]{1,2}', '', question, flags=re.IGNORECASE)
        question = re.sub(r'^[a _]+', '', question, flags=re.I)
        question = re.sub(r'[|]+', '', question)
        question = re.sub(r'[ :.,]+$', '', question)
        answer = parts[1]
        answer = re.sub(r'[|]+', '', answer)
        answer = re.sub(r'^[a-zA-Z]\. ?', '', answer)
        answer = re.sub(r'^[- ]+', '', answer)
        question = re.sub(r'[_]+[ .]?$', '', question)
        answer = re.sub(r'[ :.,]+$', '', answer)
        key_parsed = question + '|' + answer
        if question and answer and key_parsed not in existing_keys:
            final_list.append(key_parsed + '\n')
            existing_keys.add(key_parsed)
    return final_list


def parse_text_type1(file_path):
    existing_keys, raw_list = read_file(file_path)
    return parse_question_type1(existing_keys, raw_list)


def parse_question_type2(questions):
    sub = re.sub(r'^[ \[]{0,1}[0-9a-zA-Z]{1,2}[.)\]]{1}[ ]{1}', '', questions.replace('  ', ' ').replace('|', ''))
    sub = remove_unwanted(sub)
    sub = re.sub(r'^[tT]/[fF][ ]{0,2}', '', sub)
    sub = re.sub(r'^[Marks ]{1,}:[ ]{1,}[0-9 ]{1,}', '', sub)
    sub = re.sub(r'^[aA][(][n ]+[)]', '', sub)
    sub = re.sub(r'("\(Choose 1 answer\) )', '', sub, flags=re.I)
    sub = re.sub(r'(^"\d{1,}[).]{0,1}[ ]{0,1})', '', sub)
    sub = re.sub(r'(^")', '', sub)
    sub = re.sub(r'^Question[:]{0,1}[ ]{1,2}[0-9]{1,4}', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'^[ ~:]{1,99}', '', sub)
    sub = re.sub(r'^[0-9]{1,3}[)]{1}[ ]{1}', '', sub)
    sub = re.sub(r'^[0-9]{1,4}[/. ]{1,3}', '', sub)
    sub = re.sub(r'^[A-Z]{1,3}[=]{1,2}[0-9]{1,4}[ ]?', '', sub)
    sub = re.sub(r'^[(][0-9]{1,9}[)][ ]', '', sub)
    sub = re.sub(r'^[aA_ ]+', '', sub)
    sub = re.sub(r'Select one or more', '', sub, flags=re.I)
    sub = re.sub(r'Select one', '', sub, flags=re.I)
    sub = re.sub(r'Choose one or more', '', sub, flags=re.I)
    sub = re.sub(r'[( cC]{1,}hoose all that apply', '', sub, flags=re.I)
    sub = re.sub(r' ?[cC]hoose one', '', sub, flags=re.I)
    sub = re.sub(r' ?[cC]hoose two', '', sub, flags=re.I)
    sub = re.sub(r' ?[cC]hoose three', '', sub, flags=re.I)
    sub = re.sub(r'Choose one answer[. ]+', '', sub, flags=re.I)
    sub = re.sub(r'[*: ]{1,2}$', '', sub).replace('|', '')
    sub = re.sub(r'[_ .()]+$', '', sub)
    sub = re.sub(r'[*:]{1,2}[ ]{0,3}$', '', sub).replace('|', '')
    sub = re.sub(r'[01]/1', '', sub).replace('  ', ' ')
    return sub


def parse_question_type4(line):
    line = re.sub(r'^[TF/ ]{4}', '', line)
    line = re.sub(r'("(Choose 1 answer) )', '', line)
    line = re.sub(r'(^"\d{1,}[).]{0,1}[ ]{0,1})', '', line)
    line = re.sub(r'(^")', '', line)
    line = re.sub(r'^[Marks ]{1,}:[ ]{1,}[0-9 ]{1,}', '', line)
    line = re.sub(r'^[_]+[ ]?', '', line)
    line = re.sub(r'^[a-zA-Z]{2,3}[=]{1,2}[0-9 ]{1,5}', '', line)
    line = re.sub(r'^questions?:?[ ]{1,2}[0-9]{1,4}', '', line, flags=re.I)
    line = re.sub(r'^[(][0-9]{1,9}[) ]{1,3}', '', line)
    line = re.sub(r'^[#~: ]{1,4}', '', line)
    line = re.sub(r'^[0-9]{1,4}[/). ]{1,2}', '', line)
    line = re.sub(r'^[ ]+', '', line)
    line = re.sub(r'[(]?Choose one answer[)]?[. ]+', '', line, flags=re.I)
    line = re.sub(r'[*,: ]{1,2}[|]', '|', line)
    line = re.sub(r'[|][ ]+', '|', line)
    line = re.sub(r'[ ]{2,}', ' ', line)
    line = re.sub(r'[ (]{1,2}[*][) ]{1,2}[|]', '|', line)
    line = re.sub(r'[. ]+$', '', line)
    return line


def type2_first_parse(raw_list):
    answers = []
    questions = []
    question_answer = []
    for item in raw_list:
        parts = item.split(SPLITQUESTION)
        if len(parts) < 2:
            continue
        q = parts[0].replace('\n\n', '\n').replace('  ', ' ')
        a = item.replace('\n', '').replace(' ', '').split(SPLITQUESTION)[1].lower()
        a = re.sub(r'[.][ ]?.*$', '', a)
        a = re.sub(r'"[ .]*$', '', a)
        for_regex = re.split(r'[\n\[ ][a-gA-G][,.)\]][ ]?', q, flags=re.I)
        questions.append(for_regex[0].replace('\n', ' '))
        question_answer.append(for_regex)
        answers.append(a.lower())
    return questions, question_answer, answers


def parse_text_type2(file_path):
    answer_after_parse = []
    error_list = []
    pos = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 't': 'True', 'f': 'False'}
    bool_check = {'a': 'True', 'b': 'False', 't': 'True', 'f': 'False'}

    existing_keys, raw_list = read_file(file_path)
    questions, question_answer, answers = type2_first_parse(raw_list)
    final_list = []

    for i in range(len(question_answer)):
        position = pos.get(answers[i])
        try:
            if position not in ('True', 'False'):
                if 'True B. False' in question_answer[i][position]:
                    answer_after_parse.append('True')
                else:
                    answer_after_parse.append(question_answer[i][position].replace('\n', ' '))
            else:
                answer_after_parse.append(position)
        except (IndexError, TypeError):
            answer_after_parse.append(bool_check.get(answers[i], ''))

    for i in range(len(questions)):
        sub = parse_question_type2(questions[i])
        try:
            string_a = re.sub(r'[ ".]+$', '', answer_after_parse[i])
            if sub.strip() and string_a.strip():
                key_parsed = sub + '|' + string_a
                if key_parsed not in existing_keys:
                    final_list.append(key_parsed + '\n')
                    existing_keys.add(key_parsed)
        except (IndexError, TypeError):
            if len(answers[i]) > 2:
                key_parsed = sub + '|' + answers[i]
                if key_parsed not in existing_keys:
                    final_list.append(key_parsed + '\n')
                    existing_keys.add(key_parsed)
            else:
                error_list.append(sub + '|')
    return final_list, error_list


def type3(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        content = f.read()
    content = re.sub('[*]{3,}', '', content)
    content = re.sub('[~]{3,}', '', content)
    arguments = content.split(SPLITQA)
    if arguments:
        arguments.pop()
    count = 0
    skipped = 0
    with open(file_path, 'w', encoding='UTF-8') as f:
        for item in arguments:
            parts = item.split(SPLITQUESTION)
            if len(parts) < 2:
                skipped += 1
                continue
            f.write(parts[1] + SPLITQUESTION + parts[0] + SPLITQA)
            count += 1
    print(f'\n[+] Overrided position of {count} lines into File: {file_path}')
    if skipped:
        print(f'[!] Skipped {skipped} malformed entries (missing delimiter).')


def type4(file_path):
    count = 0
    form_errors = 0
    key_list = []

    with open(file_path, 'r', encoding='UTF-8') as f:
        content = f.read()
    content = re.sub(r'[ ]+\n', '\n', content)
    lines = content.split('\n')
    if lines and lines[-1] == '':
        lines.pop()

    for line in lines:
        parts = line.split('|')
        if len(parts) >= 2 and parts[0].strip() and parts[1].strip():
            key_list.append(line + '\n')
        else:
            print(f'[-] Wrong format: {line}')
            form_errors += 1

    with open(file_path + '.log', 'w', encoding='UTF-8') as f:
        for item in key_list:
            item = parse_question_type4(item.replace('  ', ' '))
            f.write(item)
            count += 1

    print(f'\n[+] Overrided {count} keys and {form_errors} key(s) in wrong form.')


if __name__ == '__main__':
    start = time.time()
    print(BANNER)

    if len(sys.argv) != 3:
        exit(HELP)

    option = sys.argv[1]
    input_file = sys.argv[2]

    if not os.path.isfile(input_file):
        exit(f'[-] File "{input_file}" not found!')

    if option == '2':
        final_list, errors = parse_text_type2(input_file)
        for err in errors:
            print(err)
        with open('key.txt', 'a', encoding='UTF-8') as f:
            for key in final_list:
                f.write(key)
        print(f'\n[+] Errors total: {len(errors)}')
        print(f'[+] Keys total wrote to file: {len(final_list)}')

    elif option == '1':
        final_list = parse_text_type1(input_file)
        with open('key.txt', 'a', encoding='UTF-8') as f:
            for key in final_list:
                f.write(key)
        print(f'\n[+] Keys total wrote to file: {len(final_list)}')

    elif option == '3':
        type3(input_file)

    elif option == '4':
        type4(input_file)

    else:
        exit('[-] Option not found!' + HELP)

    print('-------------------------------------------------------------')
    elapsed = time.time() - start
    print(f'Program executed in {elapsed:.4f} seconds')
