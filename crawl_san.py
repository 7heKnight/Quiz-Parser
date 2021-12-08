import requests
import re


def get_all_links():
    collected_links = []
    url = 'https://www.sanfoundry.com/operating-system-mcqs-cpu-scheduling-algorithms-1/'
    source = requests.get(url).text
    count = 0
    all_url = re.findall(r'href="(.+?)"', source.lower())
    all_url = list(dict.fromkeys(all_url))
    all_url.sort(reverse=True)
    for url in all_url:
        if 'operating-system' in url:
            if not ('book' in url or 'test' in url or 'rank' in url or 'json' in url or 'category' in url):
                count += 1
                collected_links.append(url)
    print(f'[*] We have {count} links')
    return collected_links


def get_question(item: str):
    try:
        question = re.search(r'^(.+?>)[ ]?a\)', item).group(1)
        question = re.sub(r'<.+?>', '', question)
        question = re.sub(r'[._? ]+$', '', question)
        question = re.sub(r'[ ]{2,}', ' ', question)
        return question
    except:
        print(f'[-] {item}')
        from sys import exit
        exit(0)


def get_answer(item: str):
    try:
        answer = re.search(r'\w$', item).group(0)
        final_answer = re.search(fr'{answer}\) (.+?)<br', item).group(1)
        return final_answer
    except:
        print(f'[-] {item}')
        from sys import exit
        exit(0)


def get_question_answer(html: str, final_key: list):
    items = re.findall(r"<p>\d+\. (.+?Answer: \w)", html)
    for item in items:
        question = get_question(item)
        answer = get_answer(item)
        final_key.append(f'{question}|{answer}')


def get_html(url: str):
    source = requests.get(url).text
    source = re.sub(r'[\r\n \t]+', ' ', source)
    return source


def write_key(list_key: list):
    with open('san_key.txt', 'w') as file:
        for key in list_key:
            file.write(key+'\n')
    print('[+] Wrote keys into: "san_key.txt"')
    file.close()


if __name__ == '__main__':
    list_links = get_all_links()
    list_key = []
    # print(source)
    for link in list_links:
        print(f'[*] Crawling on: {link}', end='')
        source = get_html(link)
        get_question_answer(source, list_key)
        print(' - Done')
        from random import randint
        from time import sleep
        sleep(0.1 * randint(1, 5))
    print(f'[+] We got {len(list_key)} keys from sanfoundry.')
    write_key(list_key)
    print('[+] Program executed successfully!')
    from sys import exit
    exit(0)

