import random
import time
import keyboard
import numpy as np
from tkinter import filedialog as fd
from tkinter import *
import tkinter.messagebox as message

import websocket_client
from tag import Tag
from websocket_client import *



tk = Tk()
WIDTHSCREEN = tk.winfo_screenwidth()
HEIGHTSCREEN = tk.winfo_screenheight()
tk.overrideredirect(True)
tk.minsize(width=int(WIDTHSCREEN / 2), height=int(HEIGHTSCREEN - HEIGHTSCREEN / 3))
tk.maxsize(width=int(WIDTHSCREEN / 2), height=int(HEIGHTSCREEN - HEIGHTSCREEN / 3))
tk.wm_geometry(
    "+%d+%d" % (int(WIDTHSCREEN / 2 - WIDTHSCREEN / 4), int(HEIGHTSCREEN / 2 - (HEIGHTSCREEN - HEIGHTSCREEN / 3) / 2)))
tk["bg"] = "light grey"

canvas = Canvas(tk, bg='white')
canvas.pack()
canvas.place(x=135, y=55, width=int(WIDTHSCREEN / 2 - 280), height=int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90))

canvas.create_rectangle(int(canvas.winfo_width()/2), 0, int(canvas.winfo_width()), int(canvas.winfo_height()/2),
                        outline='red', width=3)

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
entryWIDTH.place(x=5 + labelx.winfo_width() + 3, y=55, width=60, height=30)
entryHEIGHT = Entry(textvariable=y)
entryHEIGHT.pack()
entryHEIGHT.place(x=5 + labely.winfo_width() + 3, y=90, width=60, height=30)

listcoords = Listbox(tk, bd=3, font=("Arial", 7))
listcoords.pack()
listcoords.place(x=canvas.winfo_width() + 140, y=55, width=130, height=250)
listcoords.update()

listdangerous = Listbox(tk, bd=3, font=("Arial", 7))
listdangerous.pack()
listdangerous.place(x=canvas.winfo_width() + 140, y=310, width=130, height=250)
listdangerous.update()

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

pxinX = 0
pxinY = 0
WIDTHx = 0
HEIGHTy = 0


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
            labelmas[i]["text"] = str(round(float(HEIGHTy / 10 * (10 - i)), 2))
            labelmas[i].update()
            labelmas[i].place(x=135 - int(labelmas[i].winfo_width()),
                              y=55 - int(labelmas[i].winfo_height() / 2) + int(
                                  (HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90) / 10 * i))
        for i in range(10):
            labelmas[i + 10]["text"] = str(round(float(WIDTHx / 10 * (10 - i)), 2))
            labelmas[i + 10].update()
            labelmas[i + 10].place(
                x=135 + int((WIDTHSCREEN / 2 - 280) / 10 * (10 - i)) - int(labelmas[i].winfo_width() / 2),
                y=55 + int(HEIGHTSCREEN - HEIGHTSCREEN / 3 - 90))
        butstart["state"] = "active"
    else:
        msg = "Error input"
        message.showerror("Error", msg)


async def drawframe():
    global flag
    flag = True
    tags = []
    for line in f:
        data = line.split()
        ID = data[0]
        match_flag = 0
        for tag in tags:
            if tag.check(data):
                tag.update(data)
                tag.drawme(canvas, listcoords, pxinX, pxinY)
                if int(tag.x/pxinX)>int(canvas.winfo_width()/2) and int(tag.y/pxinY)<int(canvas.winfo_height()/2):
                    listdangerous.delete(0, 'end')
                    listdangerous.insert('end', str(ID)+str('DANGEROUS'))
                    listdangerous.itemconfig(0, {'fg': 'red'})
                else:
                    listdangerous.delete(0, 'end')

            match_flag = 1

        if match_flag == 0:
                tag = Tag(data)
                print("NEW TAG")
                tag.drawme(canvas, listcoords, pxinX, pxinY)
                tags.append(tag)
                print(tags[0].ID)
                listcoords.insert('end', str(ID) + str(" X:") + str(tag.x) + str(" Y:") + str(tag.y))
    await asyncio.sleep(0.001)
    # progstart()


def start():

    # filename = fd.askopenfilename()
    # f = open(filename, 'r')
    client = Websocket_client(websocket_client.SERVER, websocket_client.PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())
    loop.run_until_complete(drawframe())
    loop.run_forever()



def stop():
    global flag
    flag = False
    canvas.delete('target1')
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
butclose = Button(text='×', bg='red', command=close, bd=2, font=("Arial", 20))
butclose.pack()
butclose.place(x=int(WIDTHSCREEN / 2 - 30), y=5, width=25, height=25)

flag = True

maspath1x = []
maspath1y = []


def progstart():
    global flag

    butstop["state"] = "active"
    for i in range(len(board1)):
        if flag == True:
            target1X = int(int(board1[i][0]) / pxinX)
            target1Y = canvas.winfo_height() - int(int(board1[i][1]) / pxinY)
            # if (target1X>int((WIDTHSCREEN/2-280)/2) and target1Y<int((HEIGHTSCREEN-HEIGHTSCREEN/3-90)/2))
            # or (target2X>int((WIDTHSCREEN/2-280)/2) and target2Y<int((HEIGHTSCREEN-HEIGHTSCREEN/3-90)/2)):
            #   msg = "Dangerous area"
            #  message.showerror("Error", msg)
            if len(maspath1x) == 5:
                canvas.delete('path')
                del maspath1x[0]
                del maspath1y[0]
                maspath1x.append(int(int(board1[i][0]) / pxinX))
                maspath1y.append(canvas.winfo_height() - int(int(board1[i][1]) / pxinY))
                for j in range(5):
                    if j == 0:
                        canvas.create_oval(maspath1x[j] - 1, maspath1y[j] - 1, maspath1x[j] + 2, maspath1y[j] + 4,
                                           fill="red", tag='path')
                    if j == 1:
                        canvas.create_oval(maspath1x[j] - 1, maspath1y[j] - 1, maspath1x[j] + 2, maspath1y[j] + 4,
                                           fill="red", tag='path')
                    if j == 2:
                        canvas.create_oval(maspath1x[j] - 2, maspath1y[j] - 2, maspath1x[j] + 4, maspath1y[j] + 4,
                                           fill="red", tag='path')
                    if j == 3:
                        canvas.create_oval(maspath1x[j] - 2, maspath1y[j] - 2, maspath1x[j] + 4, maspath1y[j] + 4,
                                           fill="red", tag='path')
                    if j == 4:
                        canvas.create_oval(maspath1x[j] - 3, maspath1y[j] - 3, maspath1x[j] + 6, maspath1y[j] + 6,
                                           fill="red", tag='path')
            else:
                maspath1x.append(int(int(board1[i][0]) / pxinX))
                maspath1y.append(canvas.winfo_height() - int(int(board1[i][1]) / pxinY))

            canvas.delete('target1')
            canvas.create_oval(target1X - 3, target1Y - 3, target1X + 6, target1Y + 6, fill="red", tag='target1')
            listcoords.delete(0, 'end')
            listcoords.insert('end', str("SANYA - ") + str("X:") + str(board1[i][0]) + str(" Y:") + str(board1[i][1]))
            time.sleep(0.05)


tk.mainloop()
