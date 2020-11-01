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
##################################

    ###  #### #### ###   ###
    #  # #    #    #  # #
    ###  ###  ###  ###   ###
    #    #    #    # #      #
    #    #### #### #  #  ###

          ### #    ####
         #    #    #
         #    #    ###
         #    #    #
          ### #### ####

##################################
import asyncio
from multiprocessing import Process, Manager
import socket

import websockets

import reports_and_messages as rm
from config import Config
import clelib as cl
import time
from websocket_server import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# функция процесса, который расчищает буфер и кидает все данные в обработку
def MainProcessing(config, messages_buffer, web_messages_buffer):
    if config.config['log']:
        config.f = open(config.filename, 'w')
    if config.config['broadcast']:
        config.matlab_socket.connect(("mrblackdog.ddns.net", 555))
    Seq_prev = 10
    lost_number = 0

    if config.config["realtime"]:
        while True:
            if len(messages_buffer) > 0:
                mes = messages_buffer.pop(0)
                if mes.state > 0:
                    if mes.type == "Config request":
                        cl.process_config_request(mes, config)
                    if mes.type == "CS_TX" or mes.type == "CS_RX":
                        cl.process_CS(mes, config)
                    if mes.type == "BLINK":
                        cl.process_BLINK(mes, config, web_messages_buffer)

                if mes.type == "CS_TX":
                    Seq = mes.Seq
                    delta = Seq - Seq_prev
                    if delta < 0:
                        delta += 255
                    if delta > 1:
                        print("!!!!!!!! " + str(delta))
                    Seq_prev = Seq
    else:
        Tk().withdraw()
        filename = askopenfilename()
        f = open(filename, 'r')
        for line in f:
            mes = rm.MessageLog(line, config)
            if mes.state > 0:
                if mes.type == "Config request":
                    cl.process_config_request(mes, config)
                    print(config.anchors_conf)
                if mes.type == "CS_TX" or mes.type == "CS_RX":
                    cl.process_CS(mes, config)
                if mes.type == "BLINK":
                    #print(mes.rx_ID + " " + str(mes.SN) + " " + str(mes.TimeStamp))
                    cl.process_BLINK(mes, config, web_messages_buffer)

        # closing files
        f.close()
        print("END OF FILE")



# функции считвания данных с якорей, на каждый - свой процесс
def AnchorRequesting(config, i, messages_buffer):

    # socket for current anchor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.anchors_conf[i]["IP"], config.config['port']))

    # config request from current anchor
    header = s.recv(3)
    data = s.recv(500)
    mes = rm.Message(data)
    # anchors ID contained in mes and anchors number
    AnchorID = mes.tx_ID
    mes.i = i
    messages_buffer.append(mes)
    # settings for anchor
    RTLS_CMD_SET_CFG_CCP = rm.build_RTLS_CMD_SET_CFG_CCP(config.anchors_conf[i]["Master"],
                                                         config.rf_params['ch_num'],
                                                         config.rf_params['prf'],
                                                         config.rf_params['datarate'],
                                                         config.rf_params['preamble_code'],
                                                         config.rf_params['preamble_len'],
                                                         config.rf_params['pac_size'],
                                                         config.rf_params['nsfd'],
                                                         config.anchors_conf[i]["ADRx"],
                                                         config.anchors_conf[i]["ADTx"],
                                                         config.rf_params['diagnostic'],
                                                         config.rf_params['lag'])
    starttime = time.time()
    tags = []
    blinks = 0
    power = 0.
    IntegrTime = 5.
    rate = 10

    s.sendall(RTLS_CMD_SET_CFG_CCP)
    s.sendall(rm.build_RTLS_START_REQ(1))
    #for k in range(1000):
    while True:
        header = s.recv(3)
        numberofbytes = header[1]
        data = s.recv(numberofbytes)
        ending = s.recv(3)
        mes = rm.Message(data)
        if mes.type == "Unknown":
            print("ACHTUNG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(data)
            for i in data:
                print(i)
        mes.rx_ID = AnchorID
        if mes.type == "CS_TX":
            mes.tx_ID = AnchorID
        messages_buffer.append(mes)


    s.sendall(rm.build_RTLS_START_REQ(0))
    print(AnchorID + " stopped")


def start_web(cfg, message_buffer):
    server = Server(cfg, message_buffer)
    start_server = websockets.serve(server.ws_handler, cfg.server_ip, cfg.port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == "__main__":

    # load settings
    config = Config()

    messages_buffer = Manager().list()
    web_messages_buffer = Manager().list()
    processes = []
    pConsumer = Process(target=MainProcessing, args=(config, messages_buffer,web_messages_buffer))
    pConsumer.start()
    pWebConsumer = Process(target=start_web, args=(config, web_messages_buffer))
    pWebConsumer.start()

    if config.config["realtime"]:
        for i, anchor in enumerate(config.anchors_conf):
            p = Process(target=AnchorRequesting, args=(config, i, messages_buffer))
            p.start()
            processes.append(p)

    pConsumer.join()
    pWebConsumer.join()
    for p in processes:
        p.join()