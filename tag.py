import random
from math import sqrt


class Tag():
    def __init__(self, data):
        self.ID = str(data[0])
        self.color = "blue"
        self.Name = ""
        self.man = 0
        if self.ID == "dead1050b445b9":
            self.Name = "Chernyh "
            self.color = "blue"
            self.man = 1
        elif self.ID == "dead1010b44980":
            self.Name = "Malyshev"
            self.color = "blue"
            self.man = 1
        elif self.ID == "beef1050b3c216":
            self.Name = "Vehicle1"
            self.color = "black"
        else:
            self.Name = "Unknown"
        self.x = float(data[1])
        self.y = float(data[2])
        self.lat = 0.0
        self.lon = 0.0
        self.maspath = []
        self.hours = 0.
        self.message1 = ""
        self.message2 = ""

    def check(self, data):
        if (data[0]) == (self.ID):
            return True
        else:
            return False

    def update(self, data):
        self.x = float(data[1])
        self.y = float(data[2])
        self.hours = float(data[3])
        self.lat = 55.7522 + random.normalvariate(0, 0.001)
        self.lon = 37.6156 + random.normalvariate(0, 0.001)
        if self.x < 4:
            self.message2 = self.Name + " В опасной зоне"
        else:
            self.message2 = ""

    def drawme(self, canvas, listcoords, listdangerous, pxinX, pxinY, pathmasx, pathmasy, tags):
        canvas.delete('ID'+str(self.ID))
        # print(str(canvas.winfo_height()))
        # print(str(pxinX)+str("pxinX"))
        # print(str(pxinY)+str("pxinY"))
        # print(str(self.x)+str("=x"))
        # print(str(int(self.x*pxinX) - 3) + "  " + str(canvas.winfo_height()-int(self.y*pxinY) - 3) + " " + str(int(self.x*pxinX) + 6) +
        #      " " + str(canvas.winfo_height()-int(self.y*pxinY) + 6))
        canvas.create_oval(int(self.x*pxinX) - 3, canvas.winfo_height()-int(self.y*pxinY) - 3, int(self.x*pxinX) + 6,
                           canvas.winfo_height()-int(self.y*pxinY) + 6, fill=self.color, tag='ID'+str(self.ID))
        print(str((len(pathmasx))))
        canvas.delete('path')
        for j in range(len(pathmasx)):
            # for l in range(len(self.pathmasx)):
            print(str((len(pathmasx))))
            canvas.create_oval(int(pathmasx[j] * pxinX) - 3, canvas.winfo_height() - int(pathmasy[j] * pxinY) - 3,
                               int(pathmasx[j] * pxinX) + 6, canvas.winfo_height() - int(pathmasy[j] * pxinY) + 6, fill="red",
                               tag='path')

        canvas.update()
        flag = 0
        for tag1 in tags:
            if tag1.Name == "Vehicle1":
                CAR1 = tag1
                flag = 1
                break

        if self.man and flag:
            R = sqrt(pow(self.x - CAR1.x,2) + pow(self.y - CAR1.y, 2))
            print(CAR1.x)
            print(CAR1.y)
            print(self.x)
            print(self.y)
            print(R)
            if R < 1.:
                self.message1 = self.Name + "Опасность"
            else:
                self.message1 = ""

        listcoords.delete(0, 'end')
        for tag in tags:

            listcoords.insert('end', tag.Name + " RTLS: " + str(tag.x) + " " + str(tag.y) + " GPS: " + " " + str(round(tag.lat,5)) + " " + str(round(tag.lon,5)) +
                              " Смена: " + str(tag.hours) + " часов. ")

        listdangerous.delete(0, 'end')
        for tag in tags:
            if len(tag.message1) > 5:
                listdangerous.insert('end', tag.message1)
            if len(tag.message2) > 5:
                listdangerous.insert('end', tag.message2)