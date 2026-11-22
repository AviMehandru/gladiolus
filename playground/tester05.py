from piazza_api import Piazza
import time
import random
import json

p = Piazza()

with open('secrets/loginDetails.json', 'r', encoding = 'utf-8') as f:
    mySecretsDict = json.load(f)

p.user_login(email = mySecretsDict['email'], password = mySecretsDict['password'])

course = p.network(mySecretsDict['course'])

myFeed = course.get_feed(limit = 999999, offset = 0)

with open('playground/output/tester05/output.json', 'w', encoding = 'utf-8') as f:
    json.dump(myFeed, f, indent = 4)