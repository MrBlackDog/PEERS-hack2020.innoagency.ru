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
import numpy as np
import clelib as cl
import time

class Anchor():
    def __init__(self, config, i, ID):
        anch = config.anchors_conf[i]
        self.ID = ID
        self.number = i
        self.x = anch["x"]
        self.y = anch["y"]
        self.z = anch["z"]
        if anch["Master"] == 1:
            self.Range = 0.
            self.master = 1
            self.sync_flag = 1
        else:
            x = config.anchors_conf[0]["x"]
            y = config.anchors_conf[0]["y"]
            z = config.anchors_conf[0]["z"]
            self.Range = np.sqrt(pow(x - self.x, 2) + pow(y - self.y, 2) + pow(z - self.z, 2)) / config.c
            self.master = 0
            self.sync_flag = 0
        self.need_to_sync = 0
        self.X = np.array([[0.0], [0.0]])
        self.Dx = np.array([[2.46e-20, 4.21e-20], [4.21e-20, 1.94e-19]])
        self.T_rec = 0.0
        self.T_rec_last_cs = 0.0
        self.T_tx = 0.0
        self.startnumber = 5
        self.tx = []
        self.rx = []
        self.k_skip = 0 # number of skipped rx messages by raim

    def add_meas(self, config, tx, rx):
        if len(self.tx) == self.startnumber:
            del self.tx[0]
            del self.rx[0]
        self.tx.append(tx)
        self.rx.append(rx)
        if len(self.tx) == self.startnumber:
            t = []
            x = []
            for i in range(0, self.startnumber):
                t.append(self.tx[i])
                if i > 0 and t[i] - t[i-1] < 0:
                    t[i] = t[i] + config.T_max
                x.append(self.rx[i] - self.tx[i] - self.Range)
            A = np.array([[self.startnumber, 0.], [0., 0.]])
            b = np.array([[0.0], [0.0]])
            for i in range(0, self.startnumber):
                A[0][1] = A[0][1] + t[i]
                A[1][1] = A[1][1] + pow(t[i], 2)
                b[0][0] = b[0][0] + x[i]
                b[1][0] = b[1][0] + x[i] * t[i]
            A[1][0] = A[0][1]
            ax = (np.linalg.inv(A)).dot(b)
            delta = 0.
            for i in range(0, self.startnumber):
                delta = delta + pow(ax[0][0] + ax[1][0]*t[i] - x[i], 2)
            delta = np.sqrt(delta/self.startnumber)
            if delta < 3.0e-10:
                self.sync_flag = 1
                print(self.ID + " syncronized!!!")

                if config.config['log'] * config.config['CLECSSlog']:
                    data = str(time.time())
                    data += "\tCLE:\t"
                    data += str(self.number) + " " + self.ID + ": synchronized\n"
                    config.f.write(data)

                X = np.array([ax[0][0] + ax[1][0]*t[0], ax[1][0]])
                Dx = self.Dx
                for i in range(1, self.startnumber):
                    dt = self.tx[i] - self.tx[i-1]
                    if dt < 0:
                        dt = dt + config.T_max
                    b, X, Dx, nev = cl.CS_filter(X, Dx, dt, self.tx[i], self.rx[i], self.Range, config)

                #self.X[0][0] = ax[0][0] + ax[1][0]*t[len(t)-1]
                #self.X[1][0] = ax[1][0]
                self.X = X
                self.Dx = Dx
                self.T_tx = self.tx[len(self.tx)-1]
                self.tx = []
                self.rx = []



