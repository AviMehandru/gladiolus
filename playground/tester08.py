from piazza_api import Piazza
import json
import time
import random
import datetime

def setup(): 
    global p 
    global mySecretsDict
    global previousDatesDict
    global course

    global secretsPath
    global postsDirectory

    secretsPath = 'secrets/loginDetails.json'
    postsDirectory = 'playground/output/tester08/'

    p = Piazza()

    with open(secretsPath, 'r', encoding = 'utf-8') as f:
        mySecretsDict = json.load(f)

    p.user_login(email = mySecretsDict['email'], password = mySecretsDict['password'])

    course = p.network(mySecretsDict['course'])

def pullAll(): 
    dictOfPosts = {}

    postCounter = 1

    for i in course.iter_all_posts(): 
        dictOfPosts[i['nr']] = i
        time.sleep(random.randint(1, 20) / 10)
        if ((postCounter % 10) == 0): 
            print(postCounter)
        postCounter += 1

    print(f'Number of posts: {len(dictOfPosts)}')

    for i in dictOfPosts: 
        with open(f'{postsDirectory}post_{i}', 'w', encoding = 'utf-8') as f: 
            json.dump(dictOfPosts[i], f, indent = 4)
        
        try: 
            with open(f'{postsDirectory}lastUpdated.json', 'r', encoding = 'utf-8') as f: 
                oldLastUpdatedDict = json.load(f)
        except FileNotFoundError: 
            oldLastUpdatedDict = {}
        
        oldLastUpdatedDict[i] = dictOfPosts[i]['change_log'][-1]['when']

        with open(f'{postsDirectory}lastUpdated.json', 'w', encoding = 'utf-8') as f: 
            json.dump(oldLastUpdatedDict, f, indent = 4)

def pullFeed(): 
    with open(f'{postsDirectory}lastUpdated.json', 'r', encoding = 'utf-8') as f:
        previousDatesDict = json.load(f)
    
    myFeed = course.get_feed(limit = 999999, offset = 0)

    processedFeed = {}

    for i in myFeed['feed']: 
        processedFeed[i['nr']] = i['log'][-1]['t']

    fetchList = []

    for i in processedFeed: 
        if (processedFeed.get(i, None) != previousDatesDict.get(str(i), None)) and (i not in fetchList): 
            fetchList.append(i)

    postCounter = 1

    dictOfPosts = {}

    if len(fetchList) != 0: 
        for i in fetchList: 
            dictOfPosts[i] = course.get_post(i)
            time.sleep(random.randint(1, 20) / 10)
            print(postCounter)
            postCounter += 1

        for i in dictOfPosts: 
            with open(f'{postsDirectory}post_{i}', 'w', encoding = 'utf-8') as f: 
                json.dump(dictOfPosts[i], f, indent = 4)

def main(): 
    pullPostsDate = datetime.datetime.now().replace(second = 0, microsecond = 0)
    pullFeedDate = datetime.datetime.now().replace(second = 0, microsecond = 0)

    setup()
    
    while True: 
        try: 
            if datetime.datetime.now().replace(second = 0, microsecond = 0) >= pullPostsDate: 
                pullAll()

                daysToSunday = 6 - datetime.datetime.now().weekday()

                if daysToSunday <= 0:
                    daysToSunday += 7
                
                pullPostsDate = (pullPostsDate + datetime.timedelta(days = daysToSunday)).replace(hour = random.randint(5, 12), minute = random.randint(1, 59))
            if datetime.datetime.now().replace(second = 0, microsecond = 0) >= pullFeedDate.replace(second = 0, microsecond = 0): 
                pullFeed()

                pullFeedDate = pullFeedDate + datetime.timedelta(minutes = random.randint(1, 10))
        except Exception: 
            setup()
            time.sleep(10)

        time.sleep(30)

if __name__ == '__main__': 
    main()