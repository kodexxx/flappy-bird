from tkinter import *
from threading import Thread
from tkinter import messagebox
import time
import random
import sys
import os

FRAME_TIME = 0.015

current_x = 200
score = -1
truba_x = 300
diraP = 0
state = ""
finT1 = finT2 = finR = None
IS_PAUSE = 0

BEST_SCORE = 0

if os.path.isfile("data.dat"):
	scoreFile = open('data.dat')
	BEST_SCORE = int(scoreFile.read())
	scoreFile.close()
else:
	scoreFile = open('data.dat', 'w')
	scoreFile.write(str(BEST_SCORE))
	scoreFile.close()

main = Tk()
main.resizable(width = False, height = False)
main.title("Flappy Bird")


w = Canvas(main, width = 550, height = 700, background = "#4EC0CA", bd=0, highlightthickness=0)
w.pack()

birdImg = PhotoImage(file="images/bird.gif")
bird = w.create_image(100, current_x, image=birdImg)

b1 = w.create_rectangle(truba_x, 0, truba_x + 100, diraP, fill="#74BF2E", outline="#74BF2E")
b2 = w.create_rectangle(truba_x, diraP + 200, truba_x + 100, 700, fill="#74BF2E", outline="#74BF2E")
score_w = w.create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)


def updateDira():
	global diraP
	global score
	global FRAME_TIME
	
	diraP = random.randint(50, 500)
	score += 1
	w.itemconfig(score_w, text=str(score))
	if (score + 1) % 5 == 0: FRAME_TIME -= 0.001

updateDira()

def down():
	global current_x
	global truba_x
	global state
	global BEST_SCORE
	global score
	global finT1
	global finT2
	global finR
	global IS_PAUSE

	while True:
		if IS_PAUSE != True:
			if (truba_x < 150 and truba_x + 100 >= 55) and (current_x < diraP + 45 or current_x > diraP + 175):
				'''messagebox.showerror("You loose(", "You loose( Your score " + str(score))
				'''
				IS_PAUSE = True
				if score > BEST_SCORE:
					BEST_SCORE = score
					scoreFile = open('data.dat', 'w')
					scoreFile.write(str(BEST_SCORE))
					scoreFile.close()

					
				finR = w.create_rectangle(0, 0, 550, 700, fill='#4EC0CA')
				finT1 = w.create_text(15, 200, text="Your score: " + str(score), font='Impact 50', fill='#ffffff', anchor=W)
				finT2 = w.create_text(15, 280, text="Best score: " + str(BEST_SCORE), font='Impact 50', fill='#ffffff', anchor=W)

			else:
				if(state != "up"):
					if current_x < 0: current_x = 0
					if current_x > 700: current_x = 680
					w.coords(bird, 100, current_x)
					current_x = int(current_x + 9)
				truba_x -= 4
				if(truba_x <= -100): 
					truba_x = 550
					updateDira()
				w.coords(b1, truba_x, 0, truba_x + 100, diraP)
				w.coords(b2, truba_x, diraP + 200, truba_x + 100, 700)
		time.sleep(FRAME_TIME)

def up():
	global state
	global current_x

	state = "up"
	for i in range(5):
		if current_x < 0: break
		current_x = int(current_x - 17)
		w.coords(bird, 100, current_x)
		time.sleep(FRAME_TIME)
	state = "norm"	

def upKey(event = None):
	global finT1
	global finT2
	global finR
	global state
	global score
	global truba_x
	global current_x
	global IS_PAUSE
	global FRAME_TIME

	if IS_PAUSE == True:
		score = -1
		truba_x = 300
		FRAME_TIME = 0.022
		current_x = 200
		updateDira()
		w.delete(finT1)
		w.delete(finT2)
		w.delete(finR)
		IS_PAUSE = False

	elif state != "up":
		t1 = Thread(target = up)
		t1.start()

def close(event = None):
	global main
	raise SystemExit
	main.destroy()
	main.quit()
	raise SystemExit
	

t = Thread(target = down)
t.start()

main.bind("<space>", upKey)
main.bind("<Escape>", close)


mainloop()
