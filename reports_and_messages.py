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
byteorder_def = 'little'

def build_RTLS_CMD_SET_CFG_CCP(M, CP, PRF, DR, PC, PL, PSN_L, PSN_U, ADRx, ADTx, LD, Lag):
    RTLS_CMD_SET_CFG_CCP_VALUE = 0x44
    mes = RTLS_CMD_SET_CFG_CCP_VALUE.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = 0
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += M.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = CP + PRF * pow(2, 4)
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += DR.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += PC.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += PL.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = PSN_L + PSN_U * pow(2, 4)
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += ADRx.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += ADTx.to_bytes(2, byteorder=byteorder_def, signed=False)
    val = 0
    mes += val.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += LD.to_bytes(1, byteorder=byteorder_def, signed=False)
    val = 0
    mes += val.to_bytes(8, byteorder=byteorder_def, signed=False)
    mes += Lag.to_bytes(4, byteorder=byteorder_def, signed=False)
    return mes


def build_RTLS_COMM_TEST_START_REQ(Tx_Rx, Tx_frames):
    RTLS_COMM_TEST_START_REQ_VALUE = 0x53
    mes = RTLS_COMM_TEST_START_REQ_VALUE.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += Tx_Rx.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += Tx_frames.to_bytes(2, byteorder=byteorder_def, signed=False)
    return mes


def build_RTLS_ASYMM_TWR_REQ(L, IR, R, AD, TXD, RXD, RESPD, FIND, REPD, POLLPER, IADD, RADD, LN, TXPower):
    RTLS_ASYMM_TWR_REQ_VALUE = 0x55
    mes = RTLS_ASYMM_TWR_REQ_VALUE.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += L.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += IR.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += R.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += AD.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += TXD.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += RXD.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += RESPD.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += FIND.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += REPD.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += POLLPER.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += IADD.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += RADD.to_bytes(2, byteorder=byteorder_def, signed=False)
    mes += LN.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += TXPower.to_bytes(4, byteorder=byteorder_def, signed=False)

def build_RTLS_START_REQ(ON_OFF):
    RTLS_START_REQ_VALUE = 0x57
    mes = RTLS_START_REQ_VALUE.to_bytes(1, byteorder=byteorder_def, signed=False)
    mes += ON_OFF.to_bytes(1, byteorder=byteorder_def, signed=False)
    return mes

def decode_RTLS_CMD_REQ_CFG(data):
    data = data[4:12]
    ID = ""
    for i in reversed(data):
        a = str(hex(i))
        ID += a[2:]
    if len(ID) < 15:
        ID += '0'
    return ID

def decode_RTLS_COMM_TEST_RESULT_IND(data):
    return int.from_bytes(data[4:6], byteorder=byteorder_def, signed=False)


class Message():
    def __init__(self, data):
        FnCE = (data[0])
        if FnCE == 49:  # 0x31
            self.type = "CS_RX"
            self.state = 1
            data1 = data[2:10]
            ID = ""
            for i in reversed(data1):
                a = str(hex(i))
                ID += a[2:]
            if len(ID) < 15:
                ID += '0'
            self.tx_ID = ID
            self.rx_ID = ""
            self.Seq = data[1]
            self.TimeStamp = int.from_bytes(data[10:15], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
            self.FP = int.from_bytes(data[15:17], byteorder=byteorder_def, signed=False)
        elif FnCE == 50:  # 0x32
            self.type = "BLINK"
            self.state = 1
            data1 = data[2:10]
            ID = ""
            for i in reversed(data1):
                a = str(hex(i))
                ID += a[2:]
            if len(ID) < 14:
                ID += '0'
            self.tx_ID = ID
            self.rx_ID = ""
            self.SN = data[1]
            self.TimeStamp = int.from_bytes(data[10:15], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
            self.FP = int.from_bytes(data[15:17], byteorder=byteorder_def, signed=False)
            self.number = 0
        elif FnCE == 48:  # 0x30
            self.type = "CS_TX"
            self.state = 1
            self.tx_ID = ""
            self.rx_ID = ""
            self.Seq = data[1]
            self.TimeStamp = int.from_bytes(data[2:7], byteorder=byteorder_def, signed=False) * (1.0 / 499.2e6 / 128.0)
            self.FP = data[7]
        elif FnCE == 66:  # 0x42
            self.type = "Config request"
            self.state = 1
            data = data[1:9]
            ID = ""
            for i in reversed(data):
                a = str(hex(i))
                ID += a[2:]
            if len(ID) < 15:
                ID += '0'
            self.tx_ID = ID
            self.rx_ID = ID
            self.Seq = 0
            self.TimeStamp = 0
            self.FP = 0
            self.i = 0
        elif FnCE == 130:  # 0x82
            self.type = "COMM_TEST_RESULT_IND"
            self.state = 0
            self.tx_ID = "0"
            self.rx_ID = "0"
            self.Seq = 0
            self.Rx = 0
            self.FP = int.from_bytes(data[4:6], byteorder=byteorder_def, signed=False)
        else:
            self.type = "Unknown"
            self.state = 0
            self.tx_ID = "0"
            self.rx_ID = "0"
            self.Seq = 0
            self.Rx = 0
            self.FP = 0


class MessageLog():

    def __init__(self, mes, config):
        self.mes = mes
        if mes.find("New Anchor") > 0:
            self.state = 1
            self.type = "Config request"
            a = mes.split()
            self.state = 1
            self.tx_ID = a[4]
            self.rx_ID = a[4]
            self.Seq = 0
            self.TimeStamp = 0
            self.FP = 0
            self.i = int(a[3])
            config.anchors_conf[self.i]["x"] = float(a[5])
            config.anchors_conf[self.i]["y"] = float(a[6])
            config.anchors_conf[self.i]["z"] = float(a[7])
            config.anchors_conf[self.i]["Master"] = int(a[9])
        elif mes.find("CS_TX") > 0:
            self.state = 1
            self.type = "CS_TX"
            a = mes.split()
            self.tx_ID = a[2]
            self.rx_ID = a[2]
            self.Seq = int(a[4])
            self.TimeStamp = float(a[5])
            self.FP = float(a[6])
        elif mes.find("CS_RX") > 0:
            self.state = 1
            self.type = "CS_RX"
            a = mes.split()
            self.tx_ID = a[3]
            self.rx_ID = a[2]
            self.Seq = int(a[4])
            self.TimeStamp = float(a[5])
            self.FP = float(a[6])
        elif mes.find("BLINK") > 0:
            self.state = 1
            self.type = "BLINK"
            a = mes.split()
            self.tx_ID = a[3]
            self.rx_ID = a[2]
            self.SN = int(a[4])
            self.TimeStamp = float(a[5])
            self.FP = float(a[6])
            self.number = 0
        else:
            self.state = 0
            self.type = "Unknown"