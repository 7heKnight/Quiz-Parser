import sys
import re
import os

# ===== STATIC VARIABLE ===== #
KEY_AFTER_QUESTION = '$$$~~***'
KEY_AFTER_ANSWER = '***~~$$$'
KEY_FILE = 'key.txt'
ERROR_LIST = []
LIST_KEY = []

# ========================= Banner ========================= #
BANNER = r'''=============================================================================
  ___        _          ____                            |
 / _ \ _   _(_)____    |  _ \ __ _ _ __ ___  ___ _ __   |
| | | | | | | |_  /____| |_) / _` | '__/ __|/ _ \ '__|  |   
| |_| | |_| | |/ /_____|  __/ (_| | |  \__ \  __/ |     |
 \__\_\\__,_|_/___|    |_|   \__,_|_|  |___/\___|_|     |   Verion: 2
                                                        |   Made by 7heKnight
=============================================================================
''' # $figlet Quiz-Parser

HELP = fr'''- Usage: python {sys.argv[0]} <Raw_Question file>
* Export note: Custom on the left must be {KEY_AFTER_QUESTION} and the right custom is {KEY_AFTER_ANSWER}.
'''

# ====================== Output section ====================== #
def is_file_exist(file):
    try:
        open(file, 'r', encoding='utf8')
        return True
    except:
        return False

def read_file_question(file_name):
    if not is_file_exist(file_name):
        exit(f'[-] File {file_name} not found!')
    raw_text = open(file_name, 'r', encoding='utf8').read()
    return raw_text

# KEY SECTION #
def read_key():
    LIST_KEY,list_key_question, list_key_answer = [], [], []
    if not is_file_exist(KEY_FILE):
        open(KEY_FILE, 'w', encoding='utf8').close()
    quest_answer = open(KEY_FILE, 'r').read()
    quest_answer = re.findall(r'(.+?)'+chr(10), quest_answer)
    for line in quest_answer:
        LIST_KEY.append(line)
        line = line.split('|')
        list_key_question.append(line[0])
        list_key_answer.append(line[1])
    return LIST_KEY, list_key_question, list_key_answer

def write_key(new_keys):
    if not is_file_exist(KEY_FILE):
        open(KEY_FILE, 'w', encoding='utf8').close()
    file = open(KEY_FILE, 'a', encoding='utf8')
    for position in new_keys:
        file.write(position+'\n')

# !!!!!!!!!!!!!!!!!!!!!! If not in used, will remove it !!!!!!!!!!!!!!!!!!!!!! #
def output_error_key(list_questions, list_answers):
    error_file_name = 'ERROR.txt'
    file = open(error_file_name, 'w', encoding='UTF-8')
    for position in range(len(list_questions)):
        file.write(list_questions[position]+'|'+list_answers[position])

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
    parsing = re.sub(r'("\(Choose 1 answer\) )', '', parsing, re.I)
    parsing = re.sub(r'(^"\d{1,}[).]{0,1}[ ]{0,1})', '', parsing)
    parsing = re.sub(r'(^")', '', parsing)
    parsing = re.sub(r'^Question[:]{0,1}[ ]{1,2}[0-9]{1,4}|question[:]{0,1}[ ]{1,2}[0-9]{1,4}|QUESTION[:]{0,1}[ ]{1,2}[0-9]{1,4}', '', parsing, re.IGNORECASE)
    parsing = re.sub(r'^[ ~:]{1,99}', '', parsing)
    parsing = re.sub(r'^[0-9]{1,3}[)]{1}[ ]{1}', '', parsing)
    parsing = re.sub(r'^[0-9]{1,4}[/. ]{1,3}', '', parsing)
    parsing = re.sub(r'r[A-Z]{1,3}[=]{1,2}[0-9]{1,4}[ ]{0,1}', '', parsing)
    parsing = re.sub(r'^[(]{1}[0-9]{1,9}[)]{1}[ ]{1}', '', parsing)
    parsing = re.sub(r'^[aA_ ]{1,}', '', parsing)
    parsing = re.sub(r'Select one or more', '', parsing,re.I)
    parsing = re.sub(r'Select one', '', parsing,re.I)
    parsing = re.sub(r'Choose one or more', '', parsing,re.I)
    parsing = re.sub(r'[( cC]{1,}hoose all that apply', '', parsing,re.I)
    parsing = re.sub(r'[ ]{0,1}[cC]hoose one', '', parsing, re.I)
    parsing = re.sub(r'[ ]{0,1}[cC]hoose two', '', parsing, re.I)
    parsing = re.sub(r'[ ]{0,1}[cC]hoose three', '', parsing, re.I)
    parsing = re.sub(r'Choose one answer[. ]{1,}', '', parsing, re.I)
    parsing = re.sub(r'[*: ]{1,2}$', '', parsing).replace('|', '')
    parsing = re.sub(r'[_ .()]{1,}$', '', parsing)
    parsing = re.sub(r'[*:]{1,2}[ ]{0,3}$', '', parsing).replace('|', '')
    parsing = re.sub(r'[01]{1}/1', '', parsing)
    parsed_question = re.sub(r'[ ]{2,}', ' ', parsing)
    return parsed_question

def parse_answer(answer):
    parsing = re.sub(r'[|]{1,}', '', answer)
    parsing = re.sub(r'^[a-zA-Z]{1}[.]{1}[ ]{0,1}', '', parsing)
    parsing = re.sub(r'^[- ]{1,}', '', parsing)
    parsed_answer = parsing
    return parsed_answer

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
        list_questions.append(QA.split(KEY_AFTER_QUESTION)[0])
        list_answers.append(QA.split(KEY_AFTER_QUESTION)[1])
    return list_questions, list_answers

# ==== Main Section Parsing ==== #
def parse_raw_text(file_name):
    raw_text = read_file_question(file_name)
    raw_text = re.sub(r'[\n]{2,}', '\n', raw_text)
    list_questions, list_answers = parse_qa(raw_text)
    return list_questions, list_answers

# def parse_wrong_key():
#

# ====================== Selection Type ====================== #
# Type 1: Q&A, no selection
def type1(question, answer, LIST_KEY):
    key = combine_to_key(question, answer, LIST_KEY)
    return key

# Type 2: Q&A, selection choice
def type2(question, answer, LIST_KEY):
    main_question = re.sub(r'\n[a-gA-G][ .)/]{1,}.*', '', question).replace('\n', ' ')
    list_question = []
    list_answer = []
    keys = []
    getAnswer = re.findall('\w', answer, re.I)
    for choice in getAnswer:
        getAnswerInQuestion = re.search(choice + r'[. ]{1,}(.+?)[\n]|' + choice + '[. ]{1,}(.+?)$', question, re.I)
        for arguments in getAnswerInQuestion.groups():
            if arguments != None:
                list_question.append(main_question)
                list_answer.append(arguments)
                key = combine_to_key(main_question, arguments, LIST_KEY)
                keys.append(key)
    return keys # This will return a list of key

# Type 3: Wrong position, so swap them
def type3(question, answer, LIST_KEY):
    keys = type2(answer,question,LIST_KEY)
    return keys
# Type 4: True/False type
def type4(question, answer, LIST_KEY):
    if re.match('true|false', answer, re.I) == None:
        mapping_answer = {'t' : 'true', 'T' : ' true', 'f' : 'false', 'F' : 'false'}
        answer = mapping_answer.get(answer)
        key = combine_to_key(question, answer, LIST_KEY)
        return key
    key = combine_to_key(question, answer, LIST_KEY)
    return key
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
    check_true_false = re.sub(r'\S{1,}', '', answer).lower()
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
        if not key == '':
            # This need the algorithm to append key or list key
            # Need to make the STATIC_KEYS = [] and LIST_KEYS = []
            # STATIC_KEYS FOR COMPARATION, LIST_KEYS TO APPEND INTO FILE  ============ IMPORTANT =============
            if numberic_type == 1 or numberic_type == 4:
                new_keys_list.append(key)
            elif numberic_type == 2 or numberic_type == 3:
                for i in key:
                    new_keys_list.append(i)

def check_input_from_command():
    if len(sys.argv) != 2:
        exit(HELP)
    if re.search(r'help', str(sys.argv), re.I) != None or \
            re.search(r'[-]{1,2}', str(sys.argv), re.I) != None or is_file_exist(sys.argv[1]) == False:
        if is_file_exist(sys.argv[1]) == False and not ('help' in str(sys.argv) or '-h' in str(sys.argv)):
            print(f'[-] File "{sys.argv[1]}" not found!\n\n'
                  f'=============================================================================')
        exit(HELP)

# ============================ Main =========================== #
if __name__ == '__main__':
    os.system('cls')
    print(BANNER)
    check_input_from_command()
    select_type(sys.argv[1])
