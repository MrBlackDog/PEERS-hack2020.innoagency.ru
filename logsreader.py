import asyncio
import random
import time
import keyboard
import numpy as np
from tkinter import filedialog as fd
from tkinter import *
import tkinter.messagebox as message
from tag import Tag


class peers_gui():

    def __init__(self):
        self.tk = Tk()
        self.WIDTHSCREEN = self.tk.winfo_screenwidth()
        self.HEIGHTSCREEN = self.tk.winfo_screenheight()
        self.tk.overrideredirect(True)
        self.web_message_buffer =[]
        self.tk.minsize(width=int(self.WIDTHSCREEN / 2), height=int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3))
        self.tk.maxsize(width=int(self.WIDTHSCREEN / 2), height=int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3))
        self.tk.wm_geometry(
            "+%d+%d" % (int(self.WIDTHSCREEN / 2 - self.WIDTHSCREEN / 4), int(self.HEIGHTSCREEN / 2 - (self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3) / 2)))
        self.tk["bg"] = "light grey"

        self.canvas = Canvas(self.tk, bg='white')
        self.canvas.pack()
        self.canvas.place(x=135, y=55, width=int(self.WIDTHSCREEN / 2 - 280), height=int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90)/2))

        self.canvas.create_rectangle(100, 100, int(int((self.WIDTHSCREEN / 2 - 280)/10*4)), int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90)/3),
                                     outline='red', width=3)

        self.labelx = Label(text="X", bg='light grey')
        self.labely = Label(text="Y", bg='light grey')
        self.labelx.pack()
        self.labely.pack()
        self.labelx.place(x=5, y=55)
        self.labely.place(x=5, y=90)
        self.labelx.update()
        self.labely.update()

        self.x = StringVar()
        self.y = StringVar()
        self.entryWIDTH = Entry(textvariable=self.x)
        self.entryWIDTH.pack()
        self.entryWIDTH.place(x=5 + self.labelx.winfo_width() + 3, y=55, width=60, height=30)
        self.entryHEIGHT = Entry(textvariable=self.y)
        self.entryHEIGHT.pack()
        self.entryHEIGHT.place(x=5 + self.labely.winfo_width() + 3, y=90, width=60, height=30)

        self.listcoords = Listbox(self.tk, bd=3, font=("Arial", 12))
        self.listcoords.pack()
        self.listcoords.place(x=135, y=85+self.canvas.winfo_height(), width=self.canvas.winfo_width(), height=150)
        self.listcoords.update()

        self.listdangerous = Listbox(self.tk, bd=3, font=("Arial", 12))
        self.listdangerous.pack()
        self.listdangerous.place(x=135, y=85+self.canvas.winfo_height()+self.listcoords.winfo_height()+5, width=self.canvas.winfo_width(), height=150)
        self.listdangerous.update()

        self.labelmas = []

        for i in range(15):
            self.labelmas.append(Label)
        for i in range(5):
            self.labelmas[i] = Label(text=str(" "), bg='light grey')
            self.labelmas[i].pack()
            self.labelmas[i].update()
            self.labelmas[i].place(x=135 - int(self.labelmas[i].winfo_width()),
                                   y=55 - int(self.labelmas[i].winfo_height() / 2) + int(int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90)/2) / 5 * i))
        for i in range(10):
            self.labelmas[i + 5] = Label(text=str(" "), bg='light grey')
            self.labelmas[i + 5].pack()
            self.labelmas[i + 5].update()
            self.labelmas[i + 5].place(x=135 + int((self.WIDTHSCREEN / 2 - 280) / 10 * (10 - i)) - int(self.labelmas[i].winfo_width() / 2),
                                       y=55 + int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90)/2))
        self.label0 = Label(text="0", bg='light grey')
        self.label0.pack()
        self.label0.update()
        self.label0.place(x=135 - int(self.label0.winfo_width()), y=55 + int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90)/2))
        self.pxinX = 1
        self.pxinY = 1
        self.WIDTHx = 1
        self.HEIGHTy = 1
        self.butstart = Button(text='START', bg='silver', command=self.start, bd=4, font=("Arial", 9))
        self.butstop = Button(text='STOP', bg='silver', command=self.stop, bd=4, font=("Arial", 9))
        self.butstart.pack()
        self.butstop.pack()
        self.butstart.place(x=5, y=5, width=60, height=30)
        self.butstop.place(x=70, y=5, width=60, height=30)
        self.butcreate = Button(text='CREATE', bg='silver', command=self.marking, bd=4, font=("Arial", 9))
        self.butcreate.pack()
        self.butcreate.place(x=5, y=130, width=65, height=30)
        self.butstart["state"] = "disabled"
        self.butstop["state"] = "disabled"
        self.butclose = Button(text='×', bg='red', command=self.close, bd=2, font=("Arial", 20))
        self.butclose.pack()
        self.butclose.place(x=int(self.WIDTHSCREEN / 2 - 30), y=5, width=25, height=25)
        self.pathmasx=np.array([],[])
        self.pathmasy=np.array([],[])
        self.masID=[]
        self.flag=0
        self.tags = []


    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False


    def marking(self):
        self.WIDTHx = self.x.get()
        self.HEIGHTy = self.y.get()
        checkfloatWIDTH = self.isFloat(self.WIDTHx)
        checkfloatHEIGHT = self.isFloat(self.HEIGHTy)
        if checkfloatWIDTH:
            self.WIDTHx = float(self.x.get())
        if checkfloatHEIGHT:
            self.HEIGHTy = float(self.y.get())

        if (checkfloatHEIGHT and checkfloatWIDTH):
            self.canvas.create_line(3, int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90 - 3), 3, 0, width=2)
            self.canvas.create_line(3, int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90 - 3), int(self.WIDTHSCREEN / 2),
                               int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90 - 3),
                               width=2)
            for i in range(10):
                self.canvas.create_line(0, int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), 10,
                                   int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), width=2)
                self.canvas.create_line(0, int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), int(self.canvas.winfo_width()),
                                   int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90) / 10 * (i + 1)), width=1, fill="light grey")
                self.canvas.create_line(int((self.WIDTHSCREEN / 2 - 280) / 10 * (i + 1)),
                                   int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90 - 10),
                                   int((self.WIDTHSCREEN / 2 - 280) / 10 * (i + 1)), int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90),
                                   width=2)
                self.canvas.create_line(int((self.WIDTHSCREEN / 2 - 280) / 10 * (i + 1)),
                                   int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90 - int(self.canvas.winfo_height())),
                                   int((self.WIDTHSCREEN / 2 - 280) / 10 * (i + 1)), int(self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90),
                                   width=1, fill="light grey")

            self.pxinX = float(self.canvas.winfo_width() / self.WIDTHx)
            self.pxinY = float(self.canvas.winfo_height() / self.HEIGHTy)
            for i in range(5):
                self.labelmas[i]["text"] = str(round(float(self.HEIGHTy / 10 * (10 - i)), 2))
                self.labelmas[i].update()
                self.labelmas[i].place(x=135 - int(self.labelmas[i].winfo_width()),
                                       y=55 - int(self.labelmas[i].winfo_height() / 2) + int(
                                           int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90) / 2) / 5 * i))
            for i in range(10):
                self.labelmas[i + 5]["text"] = str(round(float(self.WIDTHx / 10 * (10 - i)), 2))
                self.labelmas[i + 5].update()
                self.labelmas[i + 5].place(
                    x=135 + int((self.WIDTHSCREEN / 2 - 280) / 10 * (10 - i)) - int(self.labelmas[i].winfo_width() / 2),
                    y=55 + int((self.HEIGHTSCREEN - self.HEIGHTSCREEN / 3 - 90) / 2))
            self.butstart["state"] = "active"
        else:
            msg = "Error input"
            message.showerror("Error", msg)

    def drawframe(self, line):
        global flag
        flag = True

        #for line in f:
        data = line.split()
        ID = data[0]
        match_flag = 0
        # print("!!!!!!!!"+ str(self.pxinX))
        for tag in self.tags:
            if tag.check(data):
                tag.update(data)
                # for i in range(len(self.masID)):
                #     if str(tag.ID) == self.masID[i]:
                #         flag = i
                # size=len(self.pathmasx)
                # if (size > 5):
                #     del self.pathmasx[0]
                #     del self.pathmasy[0]
                #     self.pathmasx.append(tag.x)
                #     self.pathmasy.append(tag.y)
                # else:
                #     self.pathmasx.
                #     self.pathmasy.append(tag.y)
                tag.drawme(self.canvas, self.listcoords, self.listdangerous, self.pxinX, self.pxinY, self.pathmasx, self.pathmasy, self.tags)
                # if int(tag.x/self.pxinX)>int(self.canvas.winfo_width()/2) and int(tag.y/self.pxinY)<int(self.canvas.winfo_height()/2):
                #     self.listdangerous.delete(0, 'end')
                #     self.listdangerous.insert('end', str(ID)+str('DANGEROUS'))
                #     self.listdangerous.itemconfig(0, {'fg': 'red'})
                # else:
                #     self.listdangerous.delete(0, 'end')
                match_flag = 1

        if match_flag == 0:
            tag = Tag(data)
            # self.masID.append(str(ID))
            # for i in range(len(self.masID)):
            #     if str(tag.ID)==self.masID[i]:
            #         flag=i
            # self.pathmasx[0][flag]=tag.x
            # self.pathmasy[0][flag]=tag.y
            print("NEW TAG")
            tag.drawme(self.canvas, self.listcoords, self.listdangerous, self.pxinX, self.pxinY, self.pathmasx, self.pathmasy, self.tags)
            self.tags.append(tag)
            # self.listcoords.insert('end', str(ID) + str(" X:") + str(tag.x) + str(" Y:") + str(tag.y))
            # await asyncio.sleep(0.001)
        # time.sleep(0.01)


    def start(self):
        # pass
        # filename = fd.askopenfilename()
        # f = open(filename, 'r')
        # client = Web_client(SERVER, PORT)
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(client.connect())
        # #loop.run_until_complete(drawframe())
        # loop.run_forever()
        while True:
            current_message = ""
            if len(self.web_message_buffer) > 0:
                current_message = self.web_message_buffer.pop()
                print(current_message)
                self.drawframe(current_message)




    def stop(self):
        global flag
        flag = False
        self.canvas.delete('target1')
        self.listcoords.delete(0, 'end')

    def close(self):
        self.tk.destroy()

    def progstart(self):
        global flag

        self.butstop["state"] = "active"
        for i in range(len(self.board1)):
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


#tk.mainloop()
