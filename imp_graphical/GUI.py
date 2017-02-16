from Tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk



global stereo
stereo = False


def selectStereo():
	print "stereo selected"
	global stereo
	stereo = True
def selectSingle():
	print "single selected"
	global stereo
	stereo = False


tk = Tk()

tk.title("IMP")
tk.geometry("675x525")
tk.configure(background="dark slate gray")

selectStereo() #default
print stereo



def addMenu():

	menu = Menu(tk)
	tk.config(menu=menu)
	menu.configure(background="lime green")

	modemenu = Menu(menu)
	modemenu.config(background="snow4")
	menu.add_cascade(label="settings",menu=modemenu)
	modemenu.add_command(label="mode", command=selectMode)
	modemenu.add_command(label="cameras", command=selectCamera)



def selectMode():

	window = Tk()
	window.title("mode")

	Button(window, text="Select Stereo", command=lambda : selectStereo()).grid(row=0, column=0, sticky=W, pady=4)
	Button(window, text="Select Single", command=lambda : selectSingle()).grid(row=0, column=1, sticky=W, pady=4)


def selectCamera():

	print stereo

	window = Tk()
	window.title("camera selection")

	e = Entry(window)
	e.grid(row=0, column=1)
	e.insert(5,"camera id")

	if stereo:
		e2 = Entry(window)
		e2.grid(row=1, column=1)
		e2.insert(5, "2nd camera id")



##opencv stuffs##
vc = cv2.VideoCapture(0)

imageFrame = Frame(tk, width=600, height=500)
imageFrame.grid(row=1, column=0, padx=20, pady=2)

lmain = Label(imageFrame)
lmain.grid(row=1, column=0)


def showFrame():

	_,img = vc.read()
	img = cv2.flip(img, 1)
	b,g,r = cv2.split(img)
	img = cv2.merge((r,g,b))
	im = Image.fromarray(img)
	imgtk = ImageTk.PhotoImage(image=im)

	lmain.imgtk = imgtk
	lmain.config(image=imgtk)
	lmain.after(10, showFrame)



addMenu()
showFrame()
mainloop()
