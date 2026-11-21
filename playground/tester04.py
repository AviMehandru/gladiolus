import json

with open('playground/output/tester02/allPosts', 'r', encoding = 'utf-8') as f:
    dictOfPosts = json.load(f)

for i in dictOfPosts: 
    with open(f'playground/output/tester04/post_{i}', 'w', encoding = 'utf-8') as f: 
        json.dump(dictOfPosts[i], f, indent = 4)