class Tag():
    def __init__(self, data):
        self.ID = str(data[0])
        self.x = float(data[1])
        self.y = float(data[2])

    def check(self, data):
        if str(data[0]) == str(self.ID):
            return 1
        else:
            return 0

    def update(self, data):
        self.x = float(data[1])
        self.y = float(data[2])

    def drawme(self, canvas, listcoords, pxinX, pxinY):
        canvas.delete('ID'+str(self.ID))
        canvas.create_oval(int(self.x/pxinX) - 3, canvas.winfo_height()-int(self.y/pxinY) - 3, int(self.x/pxinX) + 6,
                           canvas.winfo_height()-int(self.y/pxinY) + 6, fill="blue", tag='ID'+str(self.ID))
        canvas.update()
        # listcoords.delete(0, 'end')
        # listcoords.insert('end', str(self.ID) + str("-") + str(self.x) + str(" ") + str(self.y))
