import curses
from curses.textpad import Textbox
import re
import time 
from datetime import datetime
import requests
from PIL import Image
import os
import random
import string


def random_file():
	return ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(11))

def download_image(url):
	r = requests.get(url)
	if(r.status_code == 200):
		img = r.raw
		out_file = os.path.join('tmp',random_file())
		with open(out_file,'wb') as f:
			for chunk in r:
				f.write(chunk)
		return out_file

def images(post):
	img_tag = '<img src="URL">'
	find = re.findall(r"(https?:\/\/[^\s]*\.(?:png|jpg|webp|gif))",post)
	find = set(find)
	for f in find:
		raw_file = download_image(f)
		img = Image.open(raw_file)
		format = img.format
		img.thumbnail((640,480))
		new_file = os.path.join('img',random_file() +'.'+ format)
		img.save(os.path.join('res',new_file))
		replace_with = img_tag.replace("URL",new_file)
		post = post.replace(f,replace_with)

	return post
		

'''
title = ''
while True:
	c = stdscr.getkey()
	if c == '\n':
		break
	
	stdscr.addstr(c)
	title += c
'''

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

editwin = curses.newwin(1, curses.COLS-1, 0, 0)
box = Textbox(editwin)
box.edit()
title = box.gather()


editwin = curses.newwin(curses.LINES-2, curses.COLS-1, 1, 0)
box = Textbox(editwin)
box.edit()
post = box.gather()

YOUTUBE = '<iframe width="560" height="315" src="https://www.youtube.com/embed/LINK_CODE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

find = re.findall(r"([\w\.\:\/]*youtube\.com\/watch\?v=([a-zA-Z0-9\-\_]{11}))",post)
find += re.findall(r"([\w\.\:\/]*youtu\.be\/([a-zA-Z0-9\-\_]{11}))", post)

for f in find:
	embed = YOUTUBE.replace("LINK_CODE",f[1])
	post = post.replace(f[0],embed)

'''
IMG = '<img src="IMAGE_LINK">'

find = re.findall(r"(https?:\/\/[^\s]*\.(?:png|jpg))",post)
find = set(find)
for f in find:
	imgsrc = IMG.replace("IMAGE_LINK",f)
	post = post.replace(f,imgsrc)
'''
post = images(post)

post_lines = post.split('\n')
post = ''
cur_line = ''
for line in post_lines:
	if(len(line)==curses.COLS-1):
		cur_line += line
	else:
		post += "<p>"+cur_line+line+"<p>"
		cur_line = ''



post = "<h1>"+title+"</h1>"+post

timestamp = int(time.time())

post += datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

f = open("posts/"+str(timestamp)+".html","w")
f.write(post)
f.close()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
