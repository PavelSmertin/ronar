
__author__ = 'Pashtet <pashtetbezd@gmail.com>'


from datetime import datetime
import time
from enum import Enum

import logging
log = logging.getLogger(__name__)

TIME_INTERVAL = 40

# echo $'\n'E98D0071\"RO-TEM\"0046L0#355911044259579[1210 02 0000014B 1E]_00:30:10,01-01-2018$'\r' | nc localhost 32002

class Protocol(Enum):
    DIS = "DIS"
    DUH = "DUH"
    NAK = "NAK"
    ACK = "ACK"
    ROTEM = "RO-TEM"
    NULL = "NULL"

    @classmethod
    def has_value(cls, value):
        return (any(value == item.value for item in cls))
        
class Message():

    protocol_out = Protocol.ACK

    def __init__(self, msg):
        # CRC, 0LLL
        self.crc = msg[0:4]
        self.olll = msg[4:8]
        msg = msg[8:]

        #CRC error
        if self.crc != self.__calcCRC(msg):
            self.protocol_out = Protocol.DIS
            return

        # ID
        msg = msg[1:]
        pos = msg.index('"')
        self.protocol_in = msg[0:pos]
        msg = msg[pos+1:]

        # Seq
        self.seq = msg[0:4]
        msg = msg[4:]

        # Rrcvr
        self.rrcvr = ''
        if msg[4:] == 'R':
            pos = msg.index('L')
            self.__rrcvr = msg[0:pos]
            msg = msg[pos:]

        # Lpref
        pos = msg.index('#')
        self.lpref = msg[0:pos]
        msg = msg[pos:]

        # #acct
        pos = msg.index('[')
        self.acct = msg[0:pos]

        # timestamp
        self.msg_timestamp = msg[-19:]

        if not Protocol.has_value(self.protocol_in) :
            self.protocol_out = Protocol.DUH
            return

        if Protocol(self.protocol_in) is Protocol.NULL:
            self.protocol_out = Protocol.NAK
            return

        if not self.__checkTimestamp() :
            self.protocol_out = Protocol.NAK
            return

        if Protocol(self.protocol_in) is Protocol.ROTEM:
            self.__parseROTEM(msg[pos+1:])



    def getResponse(self):

        if self.protocol_out is Protocol.DIS:
            return

        formatter = '"{}"{}{}{}{}[]_{}'
        
        timestamp = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S,%m-%d-%Y')
        response = formatter.format(self.protocol_out.name, self.seq, self.rrcvr, self.lpref, self.acct, timestamp)

        header = ('%04x' % len(response)).upper()

        CRC = self.__calcCRC(response)
        response="\n" + CRC + header + response + "\r"
        return response

    def __checkTimestamp(self):
        currentTime = datetime.fromtimestamp(time.time())
        messageTime = datetime.strptime(self.msg_timestamp, "%H:%M:%S,%m-%d-%Y")
        return abs((currentTime - messageTime).total_seconds()) < TIME_INTERVAL

    def __parseROTEM(self, data):

        #empty data
        if(data[0:1] == "]"):
            self.protocol_out = Protocol.ACK
            return

        # data type
        self.data_type = data[0:1]

        # data code
        self.data_code = data[1:4]

        # data sensor number
        self.data_sensor_number = data[5:7]

        # data sensor value
        self.data_sensor_value = data[8:16]

        # data gsm level
        self.data_gsm_level = data[17:19]

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
