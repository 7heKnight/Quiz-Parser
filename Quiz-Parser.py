import sys
import re
import os

# ========================= Banner ========================= #
BANNER = r'''
===============================================================================
  ___        _          ____                            |
 / _ \ _   _(_)____    |  _ \ __ _ _ __ ___  ___ _ __   |
| | | | | | | |_  /____| |_) / _` | '__/ __|/ _ \ '__|  |   
| |_| | |_| | |/ /_____|  __/ (_| | |  \__ \  __/ |     |
 \__\_\\__,_|_/___|    |_|   \__,_|_|  |___/\___|_|     |   Verion: 2
                                                        |   Made by 7heKnight
===============================================================================
''' # $figlet Quiz-Parser

# ===== KEY_FOR_PARSING ===== #
KEY_AFTER_QUESTION = '$$$~~***'
KEY_AFTER_ANSWER = '***~~$$$'
ERROR_LIST = []

# ====================== Output section ====================== #
def is_file_exist(file):
    try:
        open(file, 'r', encoding='utf8')
        return True
    except:
        return False

def read_file_question(file):
    if not is_file_exist(file):
        exit(f'[-] File {file}')
    raw_text = open(file, 'r', encoding='utf8').read()
    return raw_text

# KEY SECTION #
key_file = 'key.txt'
def read_key():
    list_key,list_key_question, list_key_answer = [], [], []
    if not is_file_exist(key_file):
        open(key_file, 'w', encoding='utf8').close()
    quest_answer = open(key_file, 'r').read()
    quest_answer = re.findall(r'(.+?)'+chr(10), quest_answer)
    for line in quest_answer:
        list_key.append(line)
        line = line.split('|')
        list_key_question.append(line[0])
        list_key_answer.append(line[1])
    return list_key, list_key_question, list_key_answer

def write_key(list_key):
    if not is_file_exist(key_file):
        open(key_file, 'w', encoding='utf8').close()
    file = open(key_file, 'a', encoding='utf8')
    for position in list_key:
        file.write(position+'\n')

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
    parsing = re.sub(r'^[A-Z]{1,3}[=]{1,2}[0-9]{1,4}[ ]{0,1}', '', parsing)
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

def combine_to_key(question, answer, list_key):
    key = parse_question(question) + '|' + parse_answer(answer)
    if key in list_key:
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

# # ==== Main Section Parsing ==== #
def parse_raw_text(file):
    raw_text = read_file_question(file)
    raw_text = re.sub(r'[\n]{2,}', '\n', raw_text)
    list_questions, list_answers = parse_qa(raw_text)
    return list_questions, list_answers

# def parse_wrong_key():
#

# ====================== Selection Type ====================== #
# Type 1: Q&A, no selection
def type1(question, answer, list_key):
    key = combine_to_key(question, answer, list_key)
    return key

# # Type 2: Q&A, selection choice
# def type2():
#
# # Type 3: Wrong position, so swap them
# def type3():
#
# # Type 4: True/False type
# def type4():

# Detector
def detector(question, answer):
    type_number = 0
    if True:# Need to find some algorithm
        pass
    return type_number

# Automation select the correct type
def select_type(file_name):
    key = ''
    list_key, list_key_question, list_key_answer = read_key()
    list_questions, list_answers = parse_raw_text(file_name)
    for i in range(len(list_questions)):
        numberic_type = detector(list_questions[i], list_answers[i])
        if numberic_type == 1:
            key = type1(list_questions[i], list_answers[i], list_key)
        elif numberic_type == 2:
            pass
        elif numberic_type == 3:
            pass
        elif numberic_type == 4:
            pass
        else:
            ERROR_LIST.append(list_questions[i]+'|'+list_answers[i])
        # Check if not duplicated
        if not key == '':
            list_key.append(key)


# ============================ Main =========================== #
if __name__ == '__main__':
    print(BANNER)
    sys.exit('Just test the release version, this program has not done yet')
    #select_type(file)
    # if len(sys.argv) != 2:
    #     exit('[-] You are missing input file_name or out of range.')
