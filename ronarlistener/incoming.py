
__author__ = 'Pashtet <pashtetbezd@gmail.com>'


from datetime import datetime
import time
from enum import Enum

import logging
log = logging.getLogger(__name__)

TIME_INTERVAL = 40

# echo $'\n'E98D0071\"RO-TEM\"0046L0#355911044259579[1210 02 0000014B 1E]_00:30:10,01-01-2018$'\r' | nc localhost 32002

class Incoming():

    def __init__(self, msg):

        # Head
        # messagetype - 1 байт – Идентификатор заголовка 0х11 – сообщение 0x13 – ответ Поле messagetype 0 - сообщение, 1 - ответ
        self.messagetype = '1' if msg[0:1] == b'\x13' else '0'
        # datachannel - 1 байт – не расшифровывая лупишь туда весь байт, как есть (нолики, единички) varchar(8)
        self.datachannel = "{0:08b}".format(int(msg[1:2].hex(), 16))
        # sizebytes int
        self.sizebytes = int.from_bytes(msg[2:4], byteorder='little')
        # CRCHEAD 2 байта – Пропускаешь
        #self.crchead(msg[4:6])


        # Identities Поле идентификаторов 24 байта (передается в открытом виде)
        #self.__logHex(msg[6:30])
        # messageid int
        self.messageid = int.from_bytes(msg[6:8], byteorder='little')
        # device_iddevice int (значение всегда 1)
        self.device_iddevice = 1 # int.from_bytes(msg[8:12], byteorder='little')

        # Command
        self.command = msg[30:32].hex()

        # datetime DATETIME
        self.datetime = '20'+msg[37:38].hex()+'-'+msg[35:36].hex()+'-'+msg[36:37].hex()+' '+msg[32:33].hex()+':'+msg[33:34].hex()+':'+msg[34:35].hex()


        # Data text
        self.data = msg[38:-4].hex()
        #log.info('message')
        #log.info(msg[38:-4].hex())


        # # CRCAES
        # self.__logHex(msg[-4:-2])

        # # CRC-16
        # self.__logHex(msg[-2:])


        # fullquery
        self.fullquery = msg.hex()


    def getResponse(self):

        # if self.protocol_out is Protocol.DIS:
        #     return

        # formatter = '"{}"{}{}{}{}[]_{}'
        
        # timestamp = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S,%m-%d-%Y')
        # response = formatter.format(self.protocol_out.name, self.seq, self.rrcvr, self.lpref, self.acct, timestamp)

        # header = ('%04x' % len(response)).upper()

        # CRC = self.__calcCRC(response)
        # response="\n" + CRC + header + response + "\r"
        return #response

    def __checkTimestamp(self):
        currentTime = datetime.fromtimestamp(time.time())
        messageTime = datetime.strptime(self.msg_timestamp, "%H:%M:%S,%m-%d-%Y")
        return abs((currentTime - messageTime).total_seconds()) < TIME_INTERVAL

    def __calcCRC(self, msg):
        CRC=0
        for letter in msg:

            temp=ord(letter)
            #log.info('letter: {}, temp: {}'.format(letter, temp))

            for j in range(0,8):  # @UnusedVariable
                #log.info('j: {}'.format(j))

                temp ^= CRC & 1
                #log.info('xor temp: {}, and CRC: {}'.format(temp, CRC))

                CRC >>= 1
                #log.info('shift CRC: {}'.format(CRC))

                if (temp & 1) != 0:
                    CRC ^= 0xA001
                    #log.info('and temp: {}, xor polinom CRC: {}'.format(temp, CRC))

                #log.info('and temp: {}'.format(temp))
                temp >>= 1
                #log.info('shift temp: {}'.format(temp))
                
        return ('%x' % CRC).upper().zfill(4)

    def __encrypt(self, message):
        cipher = Blowfish.new(Config.get('encrypt_passphrase'), Blowfish.MODE_CBC, Config.get('encrypt_iv'))
        pad = 8-(len(message)%8)
        for x in range(pad):  # @UnusedVariable
            message+=" "
        encrypted = cipher.encrypt(message)
        return base64.urlsafe_b64encode(encrypted)

    def __logHex(self, msg):
        log.info( " ".join(["{:02x}".format(x).upper() for x in msg]))
