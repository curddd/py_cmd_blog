from pathlib import Path
from os import listdir
from os.path import isfile, join

HEADER = 'templates/header.html'
FOOTER = 'templates/footer.html'
CSS = 'templates/css'

POSTS = 'posts'
posts = [f for f in listdir(POSTS) if isfile(join(POSTS,f))]
posts.sort(reverse=True)

index = '<html><head>'
index += Path(HEADER).read_text()
index += '<style>'+Path(CSS).read_text()+'</style>'
index += '</head>'
index += "<body>"

for post in posts:
	index += '<div class="post">'
	index += Path(join(POSTS,post)).read_text()
	index += '</div>'
	index += "<hr>"

index += Path(FOOTER).read_text()
index += "</body></html>"


f = open("res/index.html", "w")
f.write(index)
f.close()

