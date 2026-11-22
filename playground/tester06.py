from piazza_api import Piazza
import json

p = Piazza()

with open('secrets/loginDetails.json', 'r', encoding = 'utf-8') as f:
    mySecretsDict = json.load(f)

p.user_login(email = mySecretsDict['email'], password = mySecretsDict['password'])

course = p.network(mySecretsDict['course'])

myFeed = course.get_feed(limit = 999999, offset = 0)

processedFeed = {}

for i in myFeed['feed']: 
    processedFeed[i['nr']] = i['log'][-1]['t']

with open('playground/output/tester06/output.json', 'w', encoding = 'utf-8') as f:
    json.dump(processedFeed, f, indent = 4)