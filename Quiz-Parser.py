import time
import sys
import re
SPLITQUESTION = r'"~~"'
SPLITQA= r'"**"'

BANNER = r'''
===============================================================================
  ___        _          ____                            |
 / _ \ _   _(_)____    |  _ \ __ _ _ __ ___  ___ _ __   |
| | | | | | | |_  /____| |_) / _` | '__/ __|/ _ \ '__|  |   
| |_| | |_| | |/ /_____|  __/ (_| | |  \__ \  __/ |     |
 \__\_\\__,_|_/___|    |_|   \__,_|_|  |___/\___|_|     |   Verion: 1
                                                        |   Made by 7heKnight
===============================================================================
'''

HELP = fr'''
---------------------------------------------------------------------------------------------

[*] Usage: python {sys.argv[0]} <Option number> <Question and answer in raw>
    - Option 1: Parsing the question and answer which is have the format like flashcard. It will pass the key if duplicated.
    - Option 2: Parsing the question have the multi-choice and answer is only character. It will pass the key if duplicated.
    - Option 3: Swaping the position of question and answer.
    - Option 4: Checking and removing key if each key in wrong form. (Not working)
    
---------------------------------------------------------------------------------------------

* Option 1 and 2 will append to key.txt. Option 3 will not create any but it will overriden the file. Option 4 will create the similar file with extension (*.log)

** Notes: Option have no duplicated checking so if you want to check, just use tool of Notepad++ (Edit >> Line Operation >> Remove duplicated lines.)

*** Export note: Custom on the left must be {SPLITQUESTION} and the right custom is {SPLITQA}.

'''

def removeUnwantted(sub):
    sub = re.sub(r'[(cC ]{1,}hoose 1 answer[) ]{0,1}', '', sub)
    sub = re.sub(r'[_]{1,}', '', sub)
    return sub

def readFile(dir):
    key = None
    rawList = []
    try:
        file = open('key.txt', 'r', encoding='UTF-8')
        key = file.read()
        key = re.sub('[*]{3,99}', '', key)
        key = re.sub('[~]{3,99}', '', key)
        file.close()
    except:
        pass
    try:
        f = open(dir, 'r', encoding='UTF-8')
        rawList.append(str(f.read()).split(SPLITQA))
        rawList[0].pop()
        rawList = rawList[0]
        f.close()
    except IOError:
        print('[-] Error while opening files.')
    return key, rawList

def parseQuestion_Type1(key, rawList):
    finalList = []
    for i in range(len(rawList)):
        question = rawList[i].replace('\n', ' ').replace('  ', ' ').split(SPLITQUESTION)[0]
        question = removeUnwantted(question)
        question = re.sub(r'^[# ]{1,2}', '', question)
        question = re.sub(r'^[tT]/[fF][ ]{0,2}', '', question)
        question = re.sub(r'^[_]{1,}[ ]{0,1}', '', question)
        question = re.sub(r'^[0-9]{1,3}[.) ]{1,3}', '', question)
        question = re.sub(r'^[a-z]{1,2}[=]{1}[0-9]{1,3}[ ]{1,2}', '', question, flags=re.IGNORECASE)
        question = re.sub(r'^[a _]{1,}', '', question, re.I)
        question = re.sub(r'[|]{1,}', '', question)
        question = re.sub(r'[ :.,]{1,}$', '', question)
        answer = rawList[i].replace('\n', ' ').replace('  ', ' ').split(SPLITQUESTION)[1]
        answer = re.sub(r'[|]{1,}', '', answer)
        answer = re.sub(r'^[a-zA-Z]{1}[.]{1}[ ]{0,1}', '', answer)
        answer = re.sub(r'^[- ]{1,}', '', answer)
        question = re.sub(r'[_]{1,99}[ .]{0,1}$', '', question)
        answer = re.sub(r'[ :.,]{1,99}$', '', answer)
        keyParsed = str(question)+ '|' + str(answer)
        if not (question == '' and answer == ''):
            if keyParsed in key:
                pass
            else:
                finalList.append(keyParsed + '\n')
        else:
            pass
    return finalList

def parseText_Type1(dir):
    key, rawList = readFile(dir)
    finalList = parseQuestion_Type1(key, rawList)
    return finalList

def parseQuestion_Type2(questions, key):
    sub = re.sub(r'^[ \[]{0,1}[0-9a-zA-Z]{1,2}[.)\]]{1}[ ]{1}', '', questions.replace('  ', ' ').replace('|', ''))
    sub = removeUnwantted(sub)
    sub = re.sub(r'^[tT]/[fF][ ]{0,2}', '', sub)
    sub = re.sub(r'^[Marks ]{1,}:[ ]{1,}[0-9 ]{1,}', '', sub)
    sub = re.sub(r'^[aA]{1}[(]{1}[n ]{1,}[)]{1}', '', sub)
    sub = re.sub(r'("\(Choose 1 answer\) )', '', sub, re.I)
    sub = re.sub(r'(^"\d{1,}[).]{0,1}[ ]{0,1})', '', sub)
    sub = re.sub(r'(^")', '', sub)
    sub = re.sub(r'^Question[:]{0,1}[ ]{1,2}[0-9]{1,4}|question[:]{0,1}[ ]{1,2}[0-9]{1,4}|QUESTION[:]{0,1}[ ]{1,2}[0-9]{1,4}', '', sub, re.IGNORECASE)
    sub = re.sub(r'^[ ~:]{1,99}', '', sub)
    sub = re.sub(r'^[0-9]{1,3}[)]{1}[ ]{1}', '', sub)
    sub = re.sub(r'^[0-9]{1,4}[/. ]{1,3}', '', sub)
    sub = re.sub(r'^[A-Z]{1,3}[=]{1,2}[0-9]{1,4}[ ]{0,1}', '', sub)
    sub = re.sub(r'^[(]{1}[0-9]{1,9}[)]{1}[ ]{1}', '', sub)
    sub = re.sub(r'^[aA_ ]{1,}', '', sub)
    sub = re.sub(r'Select one or more', '', sub,re.I)
    sub = re.sub(r'Select one', '', sub,re.I)
    sub = re.sub(r'Choose one or more', '', sub,re.I)
    sub = re.sub(r'[( cC]{1,}hoose all that apply', '', sub,re.I)
    sub = re.sub(r'[ ]{0,1}[cC]hoose one', '', sub, re.I)
    sub = re.sub(r'[ ]{0,1}[cC]hoose two', '', sub, re.I)
    sub = re.sub(r'[ ]{0,1}[cC]hoose three', '', sub, re.I)
    sub = re.sub(r'Choose one answer[. ]{1,}', '', sub, re.I)
    sub = re.sub(r'[*: ]{1,2}$', '', sub).replace('|', '')
    sub = re.sub(r'[_ .()]{1,}$', '', sub)
    sub = re.sub(r'[*:]{1,2}[ ]{0,3}$', '', sub).replace('|', '')
    key = re.sub(r'[01]{1}/1', '', key).replace('  ', ' ')
    return sub, key

def parseQuestion_Type4(i):
    i = re.sub(r'^[TF/ ]{4}', '', i)
    i = re.sub(r'("(Choose 1 answer) )', '', i)
    i = re.sub(r'(^"\d{1,}[).]{0,1}[ ]{0,1})', '', i)
    i = re.sub(r'(^")', '', i)
    i = re.sub(r'^[Marks ]{1,}:[ ]{1,}[0-9 ]{1,}', '', i)
    i = re.sub(r'^[_]{1,99}[ ]{0,1}', '', i)
    i = re.sub(r'^[a-zA-Z]{2,3}[=]{1,2}[0-9 ]{1,5}', '', i)
    i = re.sub(r'^[qQ][uU][eE][sS][tT][iI][oO][nN][sS]{0,1}[:]{0,1}[ ]{1,2}[0-9]{1,4}', '', i)
    i = re.sub(r'^[(]{1}[0-9]{1,9}[) ]{1,3}', '', i)
    i = re.sub(r'^[#~: ]{1,4}', '', i)
    i = re.sub(r'^[0-9]{1,4}[/). ]{1,2}', '', i)
    i = re.sub(r'^[ ]{1,99}', '', i)
    i = re.sub(r'[(]{0,1}Choose one answer[)]{0,1}[. ]{1,}', '', i, re.I)
    i = re.sub(r'[*,: ]{1,2}[|]{1}', '|', i)
    i = re.sub(r'[|]{1}[ ]{1,9}', '|', i)
    i = re.sub(r'[ ]{2,99}', ' ', i)
    i = re.sub(r'[ (]{1,2}[*]{1}[) ]{1,2}[|]{1}', '|', i)
    i = re.sub(r'[. ]{1,}$', '', i)
    return i

def type2FirstParse(rawList):
    answers = []
    questions = []
    finalList = []
    questionAnswer = []
    for i in range(len(rawList)):
        q = rawList[i].split(SPLITQUESTION)[0].replace('\n\n', '\n').replace('  ', ' ') # Changed here
        a = rawList[i].replace('\n', '').replace(' ', '').split(SPLITQUESTION)[1].lower()
        a = re.sub(r'[.]{1}[ ]{0,1}.*$', '', a)
        a = re.sub(r'"[ .]{0,}$', '', a)
        forRegex = re.split(r'[\n\[ ]{1}[a-gA-G]{1}[,.)\]]{1}[ ]{0,1}', q, flags=re.I) #here
        questions.append(forRegex[0].replace('\n', ' '))
        questionAnswer.append(forRegex)
        answers.append(a.lower())
    return finalList, questions, questionAnswer, answers

def parseText_Type2(dir):
    answerAfterParse = []
    errorList = []
    pos = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 't': 'True', 'f': 'False'}
    boolCheck = {'a': 'True', 'b': 'False', 't': 'True', 'f': 'False'}

    key, rawList = readFile(dir)
    finalList, questions, questionAnswer, answers = type2FirstParse(rawList)

    for i in range(len(questionAnswer)):
        position = pos.get(answers[i])
        try:
            if not (position == 'True' or position == 'False'):
                if 'True B. False' in questionAnswer[i][position]:
                    answerAfterParse.append('True')
                else:
                    answerAfterParse.append(questionAnswer[i][position].replace('\n', ' '))
            else:
                answerAfterParse.append(position)
        except:
            answerAfterParse.append(boolCheck.get(answers[i]))
    for i in range(len(questions)):
        sub, key = parseQuestion_Type2(questions[i], key)
        try:
            stringQ = str(sub)
            stringA = re.sub(r'[ ".]{1,}$', '', answerAfterParse[i])
            if not stringQ.replace(' ', '') == '' and not stringA.replace(' ', '') == '':
                keyParsed = str(sub) + '|' + re.sub(r'[ ".]{1,}$', '', answerAfterParse[i])
                if keyParsed in key:
                    pass
                else:
                    finalList.append(keyParsed + '\n')
            else:
                pass
        except:
            if len(answers[i]) > 2:
                keyParsed = str(sub) + '|' + answers[i]
                if keyParsed in key:
                    pass
                else:
                    finalList.append(keyParsed + '\n')
            else:
                errorList.append(str(sub)+'|')
    return finalList, errorList

def type3(dir):
    file = open(dir, 'r', encoding='UTF-8')
    arguments = file.read()
    arguments = re.sub('[*]{3,}', '', arguments)
    arguments = re.sub('[~]{3,}', '', arguments)
    file.close()
    arguments = arguments.split(SPLITQA)
    arguments.pop()
    count = 0
    try:
        file = open(dir, 'w', encoding='UTF-8')
        for i in arguments:
            file.write(i.split(SPLITQUESTION)[1] + SPLITQUESTION + i.split(SPLITQUESTION)[0] + SPLITQA)
            count += 1
        file.close()
    except Exception as e:
        print(e)
        exit('[-] Error unknown.')
    print('\n[+] Overrided position of ' + str(count) + ' lines into File: ' + dir)

def type4(dir):
    count = 0
    formE = 0
    keyList = []

    file = open(dir, 'r', encoding='UTF-8')
    arguments = file.read()
    arguments = re.sub(r'[ ]{1,}[\n]{1}', '\n', arguments)
    file.close()
    arguments = arguments.split('\n')
    arguments.pop()

    for i in arguments:
        try:
            if not i.split('|')[0] == '' and not i.split('|')[1] == '':
                keyList.append(i + '\n')
            else:
                # print('[-] Wrong format: '+i)
                print(i)
                formE += 1
        except:
            # print('[-] Wrong format1: ' + i)
            print(i)
            formE += 1
    try:
        file = open(dir+'.log', 'w', encoding='UTF-8')
        for i in keyList:
            i = parseQuestion_Type4(i.replace('  ', ' '))
            file.write(i)
            count += 1
        file.close()
    except:
        exit('[-] Error unknown.')
    print('\n[+] Overrided ' + str(count) + ' keys and ' + str(formE) + ' key in wrong form.')

if __name__=='__main__':
    start = time.time()
    print(BANNER)
    file = open('key.txt', 'a', encoding='UTF-8')
    if len(sys.argv) == 3:
        if sys.argv[1] == r'2':
            fList, error = parseText_Type2(sys.argv[2])
            count = 0
            countKey = 0
            for i in error:
                count += 1
                print(i)    # print list of error
            for i in fList:
                countKey += 1
                file.write(i)   # write key to files
            print('\n[+] Errors total: ' + str(count))
            print('[+] Keys total wrote to file: ' + str(countKey))
        elif sys.argv[1] == r'1':
            fList = parseText_Type1(sys.argv[2])
            countKey = 0
            for i in fList:
                file.write(i)
                countKey += 1
            print('\n[+] Keys total wrote to file: ' + str(countKey))
        elif sys.argv[1] == r'3':
            type3(sys.argv[2])
        elif sys.argv[1] == r'4':
            type4(sys.argv[2])
        else:
            exit('[-] Option not found!' + HELP)
    else:
        exit(HELP)
    print('-------------------------------------------------------------')
    end = time.time() - start
    time.sleep(0.0000000001)
    exit('Program executed in ' + str(end) + ' seconds')

# fr"""Notes: This is Code just applied with the parser for the answer is: {SPLITQUESTION} and next question is: {SPLITQA}"""
