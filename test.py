# PEERS RTLS Platform
# Copyright (C) NEELAR LLC, 2020
# business@neelar.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import random
import time
import keyboard
import numpy as np
from tkinter import *
import tkinter.messagebox as message
tk = Tk()
WIDTHSCREEN = tk.winfo_screenwidth()
HEIGHTSCREEN = tk.winfo_screenheight()
tk.overrideredirect(True)
tk.minsize(width=int(WIDTHSCREEN/2), height=int(HEIGHTSCREEN-HEIGHTSCREEN/3))
tk.maxsize(width=int(WIDTHSCREEN/2), height=int(HEIGHTSCREEN-HEIGHTSCREEN/3))
tk.wm_geometry("+%d+%d" % (int(WIDTHSCREEN/2-WIDTHSCREEN/4), int(HEIGHTSCREEN/2-(HEIGHTSCREEN-HEIGHTSCREEN/3)/2)))
tk["bg"] = "light grey"

canvas = Canvas(tk, bg='white')
canvas.pack()
canvas.place(x=135, y=55, width=int(WIDTHSCREEN/2-280), height=int(HEIGHTSCREEN-HEIGHTSCREEN/3-90))

#canvas.create_rectangle(int((WIDTHSCREEN/2-280)/2), 0, int(WIDTHSCREEN/2-280), int(HEIGHTSCREEN-HEIGHTSCREEN/3-90), fill='red')

labelx = Label(text="X", bg='light grey')
labely = Label(text="Y", bg='light grey')
labelx.pack()
labely.pack()
labelx.place(x=5, y=55)
labely.place(x=5, y=90)
labelx.update()
labely.update()

x = StringVar()
y = StringVar()
entryWIDTH = Entry(textvariable=x)
entryWIDTH.pack()
entryWIDTH.place(x=5+labelx.winfo_width()+3, y=55, width=60, height=30)
entryHEIGHT = Entry(textvariable=y)
entryHEIGHT.pack()
entryHEIGHT.place(x=5+labely.winfo_width()+3, y=90, width=60, height=30)

listcoords = Listbox(tk, bd=3, font=("Arial", 7))
listcoords.pack()
listcoords.place(x=canvas.winfo_width()+140, y=55, width=130, height=250)
listcoords.update()

labelmas = []
for i in range(20):
    labelmas.append(Label)
for i in range(10):
    labelmas[i] = Label(text=str(" "), bg='light grey')
    labelmas[i].pack()
    labelmas[i].update()
    labelmas[i].place(x=135 - int(labelmas[i].winfo_width()),
                      y=55 - int(labelmas[i].winfo_height() / 2) + int((HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90) / 10 * i))
for i in range(10):
    labelmas[i + 10] = Label(text=str(" "), bg='light grey')
    labelmas[i + 10].pack()
    labelmas[i + 10].update()
    labelmas[i + 10].place(x=135 + int((WIDTHSCREEN / 2 - 280) / 10 * (10 - i)) - int(labelmas[i].winfo_width() / 2),
                           y=55 + int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90))
label0 = Label(text="0", bg='light grey')
label0.pack()
label0.update()
label0.place(x=135 - int(label0.winfo_width()), y=55 + int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90))

pxinX=0
pxinY=0
WIDTHx=0
HEIGHTy=0


def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def marking():
    global x
    global y
    global pxinX
    global pxinY
    global WIDTHx
    global HEIGHTy
    WIDTHx = x.get()
    HEIGHTy = y.get()
    checkfloatWIDTH = isFloat(WIDTHx)
    checkfloatHEIGHT = isFloat(HEIGHTy)
    if checkfloatWIDTH:
        WIDTHx = float(x.get())
    if checkfloatHEIGHT:
        HEIGHTy = float(y.get())

    if (checkfloatHEIGHT and checkfloatWIDTH):
        canvas.create_line(3, int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90 - 3), 3, 0, width=2)
        canvas.create_line(3, int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90 - 3), int(WIDTHSCREEN / 2),
                           int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90 - 3),
                           width=2)
        for i in range(10):
            canvas.create_line(0, int((HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), 10,
                               int((HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), width=2)
            canvas.create_line(0, int((HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), int(canvas.winfo_width()),
                               int((HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), width=1, fill="light grey")
            canvas.create_line(int((WIDTHSCREEN / 2 - 280) / 10 * (i + 1)),
                               int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90 - 10),
                               int((WIDTHSCREEN / 2 - 280) / 10 * (i + 1)), int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90),
                               width=2)
            canvas.create_line(int((WIDTHSCREEN / 2 - 280) / 10 * (i + 1)),
                               int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90 - int(canvas.winfo_height())),
                               int((WIDTHSCREEN / 2 - 280) / 10 * (i + 1)), int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90),
                               width=1, fill="light grey")

        pxinX = float(WIDTHx / canvas.winfo_width())
        pxinY = float(HEIGHTy / canvas.winfo_height())

        for i in range(10):
            labelmas[i]["text"] = str(round(float(HEIGHTy/10*(10-i)), 2))
            labelmas[i].update()
            labelmas[i].place(x=135-int(labelmas[i].winfo_width()),
                              y=55-int(labelmas[i].winfo_height()/2)+int((HEIGHTSCREEN-HEIGHTSCREEN/3-90)/10*i))
        for i in range(10):
            labelmas[i + 10]["text"] = str(round(float(WIDTHx/10*(10-i)), 2))
            labelmas[i + 10].update()
            labelmas[i + 10].place(x=135+int((WIDTHSCREEN/2-280)/10*(10-i))-int(labelmas[i].winfo_width()/2),
                                   y=55+int(HEIGHTSCREEN-HEIGHTSCREEN/3-90))
        butstart["state"] = "active"
    else:
        msg = "Error input"
        message.showerror("Error", msg)


def start():
    global flag
    flag = True
    progstart()

def stop():
    global flag
    flag = False
    canvas.delete('target1')
    canvas.delete('target2')
    labeltarg1["text"] = " "
    labeltarg2["text"] = " "
    listcoords.delete(0, 'end')


def close():
    tk.destroy()


butstart = Button(text='START', bg='silver', command=start, bd=4, font=("Arial", 9))
butstop = Button(text='STOP', bg='silver', command=stop, bd=4, font=("Arial", 9))
butstart.pack()
butstop.pack()
butstart.place(x=5, y=5, width=60, height=30)
butstop.place(x=70, y=5, width=60, height=30)
butcreate = Button(text='CREATE', bg='silver', command=marking, bd=4, font=("Arial", 9))
butcreate.pack()
butcreate.place(x=5, y=130, width=65, height=30)
butstart["state"] = "disabled"
butstop["state"] = "disabled"
butclose = Button(text='×', bg='red',command=close, bd=2, font=("Arial", 20))
butclose.pack()
butclose.place(x=int(WIDTHSCREEN/2-30), y=5, width=25, height=25)

flag = True

target1X = 250
target1Y = 250
target2X = 100
target2Y = 100
canvas.create_rectangle(target1X, target1Y, target1X + 5, target1Y + 5, fill="red", tag='target1')
canvas.create_rectangle(target2X, target2Y, target2X + 5, target2Y + 5, fill="blue", tag='target2')
canvas.delete('target1')
canvas.delete('target2')

board1 = []
with open('log1.txt', 'r') as f:
    for row in f.read().strip().split("\n")[3:]:
        board1.append(row.split(" "))
board2 = []
with open('log2.txt', 'r') as g:
    for row in g.read().strip().split("\n")[3:]:
        board2.append(row.split(" "))

labeltarg1 = Label(text="SANYA", bg='white', font=("Arial", 7))
labeltarg2 = Label(text="VALERA", bg='white', font=("Arial", 7))

maspath1x=[]
maspath1y=[]


def progstart():
    global flag
    global target1X
    global target1Y
    global target2X
    global target2Y

    labeltarg1.pack()
    labeltarg1.place(x=250, y=250)
    labeltarg2.pack()
    labeltarg2.place(x=250, y=250)
    labeltarg1['text'] = 'SANYA'
    labeltarg2['text'] = 'VALERA'
    butstop["state"] = "active"
    for i in range(len(board1)):
        if flag==True:
            target1X = int(int(board1[i][0]) / pxinX)
            target1Y = canvas.winfo_height() - int(int(board1[i][1]) / pxinY)
            target2X = int(int(board2[i][0]) / pxinX)
            target2Y = canvas.winfo_height() - int(int(board2[i][1]) / pxinY)
            #if target1X>int((WIDTHSCREEN/2-280)/2) or target2X>int((WIDTHSCREEN/2-280)/2):
             #   msg = "Dangerous area"
              #  message.showerror("Error", msg)
            if len(maspath1x)==5:
                canvas.delete('path')
                del maspath1x[0]
                del maspath1y[0]
                maspath1x.append(int(int(board1[i][0]) / pxinX))
                maspath1y.append(canvas.winfo_height() - int(int(board1[i][1]) / pxinY))
                for j in range(5):
                    if j==0:
                        canvas.create_oval(maspath1x[j]-1, maspath1y[j]-1, maspath1x[j] + 2, maspath1y[j] + 2, fill="red", tag='path')
                    if j==1:
                        canvas.create_oval(maspath1x[j]-1, maspath1y[j]-1, maspath1x[j] + 2, maspath1y[j] + 4, fill="red", tag='path')
                    if j==2:
                        canvas.create_oval(maspath1x[j]-2, maspath1y[j]-2, maspath1x[j] + 4, maspath1y[j] + 4, fill="red", tag='path')
                    if j==3:
                        canvas.create_oval(maspath1x[j]-2, maspath1y[j]-2, maspath1x[j] + 4, maspath1y[j] + 4, fill="red", tag='path')
                    if j==4:
                        canvas.create_oval(maspath1x[j]-3, maspath1y[j]-3, maspath1x[j] + 6, maspath1y[j] + 6, fill="red", tag='path')
            else:
                maspath1x.append(int(int(board1[i][0]) / pxinX))
                maspath1y.append(canvas.winfo_height() - int(int(board1[i][1]) / pxinY))

            canvas.delete('target1')
            canvas.delete('target2')
            canvas.create_oval(target1X-3, target1Y-3, target1X + 6, target1Y + 6, fill="red", tag='target1')
            canvas.create_oval(target2X-3, target2Y-3, target2X + 6, target2Y + 6, fill="blue", tag='target2')
            listcoords.delete(0, 'end')
            listcoords.insert('end', str("SANYA - ")+str("X:")+str(board1[i][0])+str(" Y:")+str(board1[i][1]))
            listcoords.insert('end', str("VALERA - ") + str("X:") + str(board2[i][0]) + str(" Y: ")+str(board2[i][1]))
            labeltarg1.update()
            labeltarg1.place(x=target1X + 135 - labeltarg1.winfo_width()/2, y=target1Y - labeltarg1.winfo_height()-10 + 55)
            labeltarg2.update()
            labeltarg2.place(x=target2X + 135 - labeltarg2.winfo_width()/2, y=target2Y - labeltarg2.winfo_height()-10 + 55)
            time.sleep(0.05)


def texttxt():
    global target1X
    global target1Y
    global target2X
    global target2Y
    file1 = open('log1.txt', 'a')
    file2 = open('log2.txt', 'a')
    file1.write(str(target1X) + str(' ') + str(target1Y) + str('\n'))
    file2.write(str(target2X) + str(' ') + str(target2Y) + str('\n'))
    file1.close()
    file2.close()


def com(event):
    global target1X
    global target1Y
    global target2X
    global target2Y
    if event.keysym == 'w':
        target1Y = target1Y - 3
        target2Y = target2Y - 3
        #texttxt()
        canvas.delete('target1')
        canvas.delete('target2')
        canvas.create_rectangle(target1X, target1Y, target1X + 5, target1Y + 5, fill="red", tag='target1')
        canvas.create_rectangle(target2X, target2Y, target2X + 5, target2Y + 5, fill="blue", tag='target2')
        tk.update()
    else:
        if event.keysym == 's':
            target1Y = target1Y + 3
            target2Y = target2Y + 3
            #texttxt()
            canvas.delete('target1')
            canvas.delete('target2')
            canvas.create_rectangle(target1X, target1Y, target1X + 5, target1Y + 5, fill="red", tag='target1')
            canvas.create_rectangle(target2X, target2Y, target2X + 5, target2Y + 5, fill="blue", tag='target2')
            tk.update()
        else:
            if event.keysym == 'a':
                target1X = target1X - 3
                target2X = target2X - 3
                #texttxt()
                canvas.delete('target1')
                canvas.delete('target2')
                canvas.create_rectangle(target1X, target1Y, target1X + 5, target1Y + 5, fill="red", tag='target1')
                canvas.create_rectangle(target2X, target2Y, target2X + 5, target2Y + 5, fill="blue", tag='target2')
                tk.update()
            else:
                if event.keysym == 'd':
                   target1X = target1X + 3
                   target2X = target2X + 3
                   #texttxt()
                   canvas.delete('target1')
                   canvas.delete('target2')
                   canvas.create_rectangle(target1X, target1Y, target1X + 5, target1Y + 5, fill="red", tag='target1')
                   canvas.create_rectangle(target2X, target2Y, target2X + 5, target2Y + 5, fill="blue", tag='target2')
                   tk.update()


tk.bind("<Key>", com)
tk.mainloop()
