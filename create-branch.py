import requests
import yaml
import os
import sys
import json
from pathlib import Path

#
# Here some sample values to set in git.yml
# - Authorization: token abcde49ccabcd0dfe7298e3a4d62faeaaaaabbbb
# - Authorization: basic aaaabbbbccccddddLWNvZGVyb2FkLWNvbTpyM25Abmh1QG5jYQ==
# for token authorization more information can be found here: https://developer.github.com/v3/oauth_authorizations/ 
#

credentials_path = "%s/.credentials/git.yml" % Path.home()
if not os.path.exists(credentials_path):
    print("error: git credentials file [%s] does not exists." % credentials_path)
    sys.exit()

authorization = None
with open(credentials_path, "r") as f:
    docs = yaml.load(f)
    try:
        authorization = docs['Authorization']
    except:
        print("error: Authorization not set.")
        sys.exit()

headers = {
    "Authorization": authorization,
    "Accept": "application/vnd.github.v3+json"
}

if(len(sys.argv) < 5):
    print("usage: python3 create-branch.py user branch1 branch2")
    sys.exit()

user = sys.argv[1]
repo = sys.argv[2]
from_branch = sys.argv[3]
to_branch = sys.argv[4]

print("user:", user)
print("repo:", repo)
print("from_branch:", from_branch)
print("to_branch:", to_branch)

r1 = requests.get('https://api.github.com/repos/%s/%s/branches/%s' % (user, repo, from_branch), 
                 headers=headers)

revision = r1.json()['commit']['sha']
print()
print(r1.status_code)
print("source revision: ", revision)

payload = {
    'ref': "refs/heads/%s" % (to_branch),
    'sha': revision
}

r2 = requests.post("https://api.github.com/repos/%s/%s/git/refs" % (user, repo), 
                 headers=headers,
                 data= json.dumps(payload)
                 )

print(r2.status_code)
print(r2.json())

# revision = r1.json()['commit']['sha']

