from piazza_api import Piazza
import json
import time
import random

p = Piazza()

with open('secrets/loginDetails.json', 'r', encoding = 'utf-8') as f:
    mySecretsDict = json.load(f)

with open('playground/output/tester06/output.json', 'r', encoding = 'utf-8') as f:
    previousDatesDict = json.load(f)

p.user_login(email = mySecretsDict['email'], password = mySecretsDict['password'])

course = p.network(mySecretsDict['course'])

myFeed = course.get_feed(limit = 999999, offset = 0)

processedFeed = {}

for i in myFeed['feed']: 
    processedFeed[i['nr']] = i['log'][-1]['t']

fetchList = []

if len(previousDatesDict) != len(processedFeed): 
    for i in processedFeed: 
        if previousDatesDict.get(i, None) is None: 
            fetchList.append(i)

for i in processedFeed: 
    if processedFeed.get(i, None) != previousDatesDict.get(str(i), None): 
        fetchList.append(i)
        print(f'b{i}: {processedFeed.get(i, None)}, {previousDatesDict.get(str(i), None)}, dtypes: {type(i)}, {type(processedFeed.get(i, None))}', {type(previousDatesDict.get(i, None))})

postCounter = 1

dictOfPosts = {}

if len(fetchList) != 0: 
    for i in fetchList: 
        dictOfPosts[i] = course.get_post(i)
        time.sleep(random.randint(1, 20) / 10)
        print(postCounter)
        postCounter += 1

    with open('playground/output/tester07/fetchDict.json', 'w', encoding = 'utf-8') as f:
        json.dump({'fetchList': fetchList}, f, indent = 4)

    with open('playground/output/tester07/newPosts.json', 'w', encoding = 'utf-8') as f:
        json.dump(dictOfPosts, f, indent = 4)