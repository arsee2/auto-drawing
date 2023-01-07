import cv2 as cv 
from matplotlib import pyplot as plt 
from skimage.morphology import skeletonize
import time
import numpy as np
import pyautogui
from prompt_toolkit.key_binding import KeyBindings
from tkinter import *
bindings = KeyBindings()
import win32api, win32con
import queue

import sys
sys.setrecursionlimit(100000)

count=1


def dfs(img,x,y,arr,visited):
	global count
	count+=1
	visited[x][y] = 1
	arr.append((y,x))
	for i in range(-1,2):
		for j in range(-1,2):
			if x+i<0 or x+i>=len(img) or y+j<0 or y+j>=len(img[0]):
				continue
			if visited[x+i][y+j]>0:
				continue
			visited[x+i][y+j]=1
			if img[x+i][y+j]>0:
				dfs(img,x+i,j+y,arr,visited)
	count-=1
	print(count)

def dfs(img,xi,yi,arr,visited):
	s = []
	s.append((xi,yi))
	while len(s)>0:
		x,y = s[-1]
		s.pop()
		visited[x][y] = 1
		arr.append((y,x))
		for i in range(-1,2):
			for j in range(-1,2):
				if x+i<0 or x+i>=len(img) or y+j<0 or y+j>=len(img[0]):
					continue
				if visited[x+i][y+j]>0:
					continue
				visited[x+i][y+j]=1
				if img[x+i][y+j]>0:
					s.append((x+i,y+j))

def get_paths(img):
	paths = []
	visited = np.zeros(img.shape)
	for i in range(len(img)):
		for j in range(len(img[0])):
			if img[i][j]>0 and visited[i][j]==0:
				cur = []
				dfs(img,i,j,cur,visited)
				paths.append(cur)
	return paths
			
def finish():
	exit()

def split_paths(paths):
	answer = []
	for path in paths:
		if len(path)<25:
			continue
		answer.append([])
		px , py = path[0]
		for x,y in path:
			if abs(x-px)>2 or abs(y-py)>2:
				answer.append([])
			answer[-1].append((x,y))
			px = x
			py = y
	#print(answer)
	return answer

def draw(arg):
	img = cv.imread("img.jpg")
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	width , height = img.shape
	max_len = 300
	if width>height:
		height = max_len/width*height
		width = max_len
	else:
		width = max_len/height*width
		height = max_len
	img = cv.resize(img, (int(height),int(width)), interpolation = cv.INTER_AREA)
	
	img = cv.GaussianBlur(img,(5,5),0)
	#img = cv.Canny(img,10,25)
	img =  cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,7,2)

	img = 255 - img
	img[img>0]=1
	#plt.imshow(img)
	#plt.show()
	#img = skeletonize(img)
	ix, iy = pyautogui.position()
	cnt=0
	paths = get_paths(img)
	paths = split_paths(paths)

	z = np.zeros(img.shape)
	for path in paths:
		bx , by = path[0]
		win32api.SetCursorPos((bx+ix,by+iy))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,bx+ix,by+iy,0,0)
		#time.sleep(0.001)
		for x,y in path:
			z[y][x] = 1
			cnt+=1
			if cnt>1000000:
				break
			win32api.SetCursorPos((ix+x,iy+y))
			for j in range(10000):
				p = cnt/3
   
   
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,ix+x,y+iy,0,0)
		#time.sleep(0.001)
	plt.imshow(z)
	plt.show()
	plt.imshow(img)
	plt.show()
			
	

window = Tk()
window.geometry("600x400")
window.title("Test")


window.bind("a", draw)

window.bind("e", exit)

window.mainloop()