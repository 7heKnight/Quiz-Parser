import sys
import re
import os

# ===== STATIC VARIABLE ===== #
KEY_AFTER_QUESTION = '$$$~~***'
KEY_AFTER_ANSWER = '***~~$$$'
KEY_FILE = 'key.txt'
ERROR_LIST = []

# ========================= Banner ========================= #
BANNER = r'''=============================================================================
  ___        _          ____                            |
 / _ \ _   _(_)____    |  _ \ __ _ _ __ ___  ___ _ __   |
| | | | | | | |_  /____| |_) / _` | '__/ __|/ _ \ '__|  |   
| |_| | |_| | |/ /_____|  __/ (_| | |  \__ \  __/ |     |
 \__\_\\__,_|_/___|    |_|   \__,_|_|  |___/\___|_|     |   Version: 2
                                                        |   Made by 7heKnight
=============================================================================
''' # $figlet Quiz-Parser

HELP = fr'''- Usage: python {sys.argv[0]} <Raw_Question file>
* Export note: Custom on the left must be {KEY_AFTER_QUESTION} and the right custom is {KEY_AFTER_ANSWER}.
'''

# ====================== Output section ====================== #
def is_file_exist(file):
    return os.path.isfile(file)

def read_file_question(file_name):
    if not is_file_exist(file_name):
        exit(f'[-] File {file_name} not found!')
    with open(file_name, 'r', encoding='utf8') as f:
        return f.read()

# KEY SECTION #
def read_key():
    list_key, list_key_question, list_key_answer = [], [], []
    if not is_file_exist(KEY_FILE):
        open(KEY_FILE, 'w', encoding='utf8').close()
        return list_key, list_key_question, list_key_answer
    with open(KEY_FILE, 'r', encoding='utf8') as f:
        lines = re.findall(r'(.+?)\n', f.read())
    for line in lines:
        list_key.append(line)
        parts = line.split('|')
        if len(parts) >= 2:
            list_key_question.append(parts[0])
            list_key_answer.append(parts[1])
    return list_key, list_key_question, list_key_answer

def write_key(new_keys):
    with open(KEY_FILE, 'a', encoding='utf8') as f:
        for position in new_keys:
            f.write(position + '\n')

# ==================== Checking & Parsing ==================== #
# === This section is child === #
def parse_question(question):
    parsing = re.sub(r'[\n]{1,}', ' ', question)
    parsing = re.sub(r'[ ]{2,}', ' ', parsing)
    parsing = re.sub(r'[|]{1,}', ' ', parsing)
    parsing = re.sub(r'^[ \[]{0,1}[0-9a-zA-Z]{1,2}[.)\]]{1}[ ]{1}', '', parsing)
    parsing = re.sub(r'[(cC ]{1,}hoose 1 answer[) ]{0,1}', '', parsing)
    parsing = re.sub(r'[_]{1,}', '', parsing)
    parsing = re.sub(r'^[tT]/[fF][ ]{0,2}', '', parsing)
    parsing = re.sub(r'^[Marks ]{1,}:[ ]{1,}[0-9 ]{1,}', '', parsing)
    parsing = re.sub(r'^[aA]{1}[(]{1}[n ]{1,}[)]{1}', '', parsing)
    parsing = re.sub(r'("\(Choose 1 answer\) )', '', parsing, flags=re.I)
    parsing = re.sub(r'(^"\d{1,}[).]{0,1}[ ]{0,1})', '', parsing)
    parsing = re.sub(r'(^")', '', parsing)
    parsing = re.sub(r'^Question[:]{0,1}[ ]{1,2}[0-9]{1,4}', '', parsing, flags=re.IGNORECASE)
    parsing = re.sub(r'^[ ~:]{1,99}', '', parsing)
    parsing = re.sub(r'^[0-9]{1,3}[)]{1}[ ]{1}', '', parsing)
    parsing = re.sub(r'^[0-9]{1,4}[/. ]{1,3}', '', parsing)
    parsing = re.sub(r'r[A-Z]{1,3}[=]{1,2}[0-9]{1,4}[ ]{0,1}', '', parsing)
    parsing = re.sub(r'^[(]{1}[0-9]{1,9}[)]{1}[ ]{1}', '', parsing)
    parsing = re.sub(r'^[aA_ ]{1,}', '', parsing)
    parsing = re.sub(r'Select one or more', '', parsing, flags=re.I)
    parsing = re.sub(r'Select one', '', parsing, flags=re.I)
    parsing = re.sub(r'Choose one or more', '', parsing, flags=re.I)
    parsing = re.sub(r'[( cC]{1,}hoose all that apply', '', parsing, flags=re.I)
    parsing = re.sub(r'[ ]{0,1}[cC]hoose one', '', parsing, flags=re.I)
    parsing = re.sub(r'[ ]{0,1}[cC]hoose two', '', parsing, flags=re.I)
    parsing = re.sub(r'[ ]{0,1}[cC]hoose three', '', parsing, flags=re.I)
    parsing = re.sub(r'Choose one answer[. ]{1,}', '', parsing, flags=re.I)
    parsing = re.sub(r'[*: ]{1,2}$', '', parsing).replace('|', '')
    parsing = re.sub(r'[_ .()]{1,}$', '', parsing)
    parsing = re.sub(r'[*:]{1,2}[ ]{0,3}$', '', parsing).replace('|', '')
    parsing = re.sub(r'[01]{1}/1', '', parsing)
    parsed_question = re.sub(r'[ ]{2,}', ' ', parsing)
    return parsed_question

def parse_answer(answer):
    parsing = re.sub(r'[|]{1,}', '', answer)
    parsing = re.sub(r'^[a-zA-Z]{1}[.]{1}[ ]{0,1}', '', parsing)
    return re.sub(r'^[- ]{1,}', '', parsing)

def combine_to_key(question, answer, LIST_KEY):
    key = parse_question(question) + '|' + parse_answer(answer)
    if key in LIST_KEY:
        key = ''
    return key

def parse_qa(raw_text):
    QuestionAnswer = raw_text.split(KEY_AFTER_ANSWER)
    QuestionAnswer.pop()
    list_questions, list_answers = [], []
    for QA in QuestionAnswer:
        parts = QA.split(KEY_AFTER_QUESTION)
        if len(parts) < 2:
            continue  # skip malformed blocks missing the question delimiter
        list_questions.append(parts[0])
        list_answers.append(parts[1])
    return list_questions, list_answers

# ==== Main Section Parsing ==== #
def parse_raw_text(file_name):
    raw_text = read_file_question(file_name)
    raw_text = re.sub(r'[\n]{2,}', '\n', raw_text)
    list_questions, list_answers = parse_qa(raw_text)
    return list_questions, list_answers

# ====================== Selection Type ====================== #
# Type 1: Q&A, no selection
def type1(question, answer, LIST_KEY):
    key = combine_to_key(question, answer, LIST_KEY)
    return key

# Type 2: Q&A, selection choice
def type2(question, answer, LIST_KEY):
    main_question = re.sub(r'\n[a-gA-G][ .)/]{1,}.*', '', question).replace('\n', ' ')
    keys = []
    getAnswer = re.findall('\w', answer, re.I)
    for choice in getAnswer:
        getAnswerInQuestion = re.search(choice + r'[. )/\\]{1,}(.+?)[\n]|' + choice + r'[. )/\\]{1,}(.+?)$', question, re.I)
        if getAnswerInQuestion is None:
            continue  # choice letter not found in question options — skip
        for arguments in getAnswerInQuestion.groups():
            if arguments is not None:
                key = combine_to_key(main_question, arguments, LIST_KEY)
                keys.append(key)
    return keys

# Type 3: Wrong position, so swap them
def type3(question, answer, LIST_KEY):
    try:
        return type2(answer, question, LIST_KEY)
    except Exception as e:
        print(f'[!] type3 swap failed — {e}')
        return []
# Type 4: True/False type
def type4(question, answer, LIST_KEY):
    if re.match('true|false', answer, re.I) is None:
        mapping_answer = {'t': 'true', 'T': 'true', 'f': 'false', 'F': 'false'}
        answer = mapping_answer.get(answer, answer)  # fallback to original to avoid None
    return combine_to_key(question, answer, LIST_KEY)
# Need type_5, detect the multi question and answer is the answer, not A or B or C or D or etc..
def type5(question, answer, LIST_KEY):
    pass


# Detector
def detector(question, answer): # Not checked already, not sure if it works
    if (len(question) <= 4):
        return 3
    elif (question.count('\n') >= 3 and len(answer) <=4):
        return 2
    elif (question.count('\n') == 0):
        return 1
    check_true_false = re.sub(r'\s{1,}', '', answer).lower()
    if 't' ==  check_true_false or 'f'== check_true_false or check_true_false == 'true' or check_true_false == 'false':
        return 4
    check_type_5 = re.sub(r'[a-gA-G][,.)/\\ ]{1,}', '', answer)
    if check_type_5 in question:
        return 5
    return -1

# Automation select the correct type
def select_type(file_name):
    key = ''
    new_keys_list = []
    LIST_KEY, list_key_question, list_key_answer = read_key()
    list_questions, list_answers = parse_raw_text(file_name)
    for i in range(len(list_questions)):
        numberic_type = detector(list_questions[i], list_answers[i])
        if numberic_type == 1:
            key = type1(list_questions[i], list_answers[i], LIST_KEY)
        elif numberic_type == 2:
            key = type2(list_questions[i], list_answers[i], LIST_KEY)
        elif numberic_type == 3:
            key = type3(list_questions[i], list_answers[i], LIST_KEY)
        elif numberic_type == 4:
            key = type4(list_questions[i], list_answers[i], LIST_KEY)
        else:
            ERROR_LIST.append(list_questions[i]+'|'+list_answers[i])
        # Check if not duplicated
        # Checking key, if key = list so use for loop, otherwise, use below syntax  ============ IMPORTANT =============
        if key:
            if numberic_type == 1 or numberic_type == 4:
                new_keys_list.append(key)
            elif numberic_type == 2 or numberic_type == 3:
                for entry in key:
                    new_keys_list.append(entry)
    write_key(new_keys_list)
    if ERROR_LIST:
        print(f'[!] {len(ERROR_LIST)} entries could not be parsed.')

def check_input_from_command():
    if len(sys.argv) != 2:
        exit(HELP)
    arg = sys.argv[1]
    if arg in ('-h', '--help', 'help') or not is_file_exist(arg):
        if not is_file_exist(arg) and arg not in ('-h', '--help', 'help'):
            print(f'[-] File "{arg}" not found!\n\n'
                  f'=============================================================================')
        exit(HELP)

# ============================ Main =========================== #
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    check_input_from_command()
    select_type(sys.argv[1])
