from piazza_api import Piazza
import json

p = Piazza()

with open('secrets/loginDetails.json', 'r', encoding = 'utf-8') as f:
    mySecretsDict = json.load(f)

with open('secrets/myPosts.json', 'r', encoding = 'utf-8') as f: 
    myPost = json.load(f)

p.user_login(email = mySecretsDict['email'], password = mySecretsDict['password'])

course = p.network(mySecretsDict['course'])

post = course.get_post(myPost['example1'])

subject = post['history'][0]['subject']
content = post['history'][0]['content']
created_at = post['created']
tags = post['folders']

print('Details:\n')
print(f'Subject: {subject}')
print(f'Folders: {tags}')
print(f'Created: {created_at}')
print(f'Content (HTML):\n{content}')

print('Post:\n')
print(post)