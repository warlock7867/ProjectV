import requests
import sys

url = sys.argv[1]
name = sys.argv[2]


print("getting webpage...")
r = requests.get(url)
with open("html/%s.html"%name, "w", encoding = 'utf-8') as file:
    code = r.text
    file.write(code)
    print("saving into folder...")
    file.close()

print("done...")