import html
import sys

path = sys.argv[1]

with open(path, 'r') as content_file:
    content = content_file.read()

content_ = html.unescape(content)

with open(path, 'w') as content_file:
    content_file.write(content_)