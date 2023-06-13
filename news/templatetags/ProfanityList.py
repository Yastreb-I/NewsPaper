import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
words_file = os.path.join(BASE_DIR, 'words.txt')

with open(words_file, 'r', encoding='utf-8') as f:
    censor_list = [line.strip() for line in f.readlines()]


def profanity_redactor(value):
    variants = censor_list  # непристойные выражения
    ln = len(variants)
    filtred_message = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    for i in value:
        string += i
        string2 = string.lower()

        flag = 0
        for j in variants:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_message += pattern * len(string)
                flag -= 1
                string = ''

        if flag == ln:
            filtred_message += string
            string = ''

    if string2 != '' and string2 not in variants:
        filtred_message += string
    elif string2 != '':
        filtred_message += pattern * len(string)

    return filtred_message
