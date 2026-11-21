from piazza_api import Piazza
import time
import random
import json

p = Piazza()

with open('secrets/loginDetails.json', 'r', encoding = 'utf-8') as f:
    mySecretsDict = json.load(f)

p.user_login(email = mySecretsDict['email'], password = mySecretsDict['password'])

course = p.network(mySecretsDict['course'])

dictOfPosts = {}

postCounter = 1

for i in course.iter_all_posts(): 
    dictOfPosts[i['nr']] = i
    time.sleep(random.randint(1, 20) / 10)
    if ((postCounter % 10) == 0): 
        print(postCounter)
    postCounter += 1

print(f'Number of posts: {len(dictOfPosts)}')

with open('playground/output/tester02/allPosts', 'w', encoding = 'utf-8') as f: 
    json.dump(dictOfPosts, f, indent = 4)