# -*- coding: utf-8 -*-

import os
import json
import string
import collections


def getInputParameters():
    print('I want N-top chart of the most frequent L-long words')
    chart = None
    lengh = 1
    while(True):
        chart = input('N = ')
        length = input('L = ')
        print()
        if chart == None or chart.isdigit() != True:
            print('Int number needed. Try again\n')
            continue
        if length == None or length.isdigit() != True:
            print('Int number needed. Try again\n')
            continue
        else:
            return int(chart), int(length)
            break



def getJsonchick():
    file = open('dump.json', mode='r', encoding='utf-8')
    raw_data = json.load(file)
    return raw_data

def getUserID(data):
    user_id = data['personal_information'].get('user_id')
    return user_id


def getContactsChat(data):
    contacts = {}
    messageCount = [0, 0] # the first is for user's messages, the second is for recipient

    for i in data['chats']['list'][1:]:
        name = i['name']
        if i['name'] == '':
            name = 'Unknown contact'
        contacts[name] = i['id']
        for j in data['chats']['list'][1:]:
                for info in j['messages']:
                    if info.get('from_id') == contacts[name]:
                        messageCount[0] += 1
                    else:
                        messageCount[1] += 1        
        messageCount = [0,0]


def getMessages(data, user):
    messages = []
    for i in data['chats']['list'][1:]:
        for j in i['messages']:
            if j.get('from_id') == user:
                if not isinstance(j.get('text'), str):
                        continue
                else:
                    messages.append(j.get('text'))

    os.system('cls')    
    return messages

def getCounter(messages, *params):
    counter = collections.Counter()
    l = params
    chart = l[0][0]
    length = l[0][1]

    for message in messages:
        raw_words = message.split(' ')        
        for word in raw_words:
            clear_word = word.strip(string.punctuation+string.whitespace).lower()            
            if len(clear_word) == length:                
                counter[clear_word] += 1
            else:
                continue

    for i in counter.most_common(chart):
        print(i[0], ':', i[1], 'times.')


def start():    
    raw_data = getJsonchick()
    user_id = getUserID(raw_data)
    messages = getMessages(raw_data, user_id)
    getCounter(messages, getInputParameters())
    getContactsChat(raw_data)

    input('\n\nPress ENTER to quit...')


if __name__ == '__main__':
    start()
