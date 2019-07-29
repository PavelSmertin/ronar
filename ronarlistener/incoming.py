
__author__ = 'Pashtet <pashtetbezd@gmail.com>'



from enum import Enum
import crcmod

import logging
log = logging.getLogger(__name__)

TIME_INTERVAL = 40

# echo $'\n'E98D0071\"RO-TEM\"0046L0#355911044259579[1210 02 0000014B 1E]_00:30:10,01-01-2018$'\r' | nc localhost 32002

class Incoming():

    def __init__(self, msg = None):

        if msg == None: 
            return

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
        self.messageidByte = msg[6:8]
        self.messageid = int.from_bytes(msg[6:8], byteorder='little')
        # device_iddevice int (значение всегда 1)
        self.device_iddevice = 1 # int.from_bytes(msg[8:12], byteorder='little')

        # Command
        self.commandByte = msg[30:32]
        self.command = msg[30:32].hex()

        # datetime DATETIME
        self.datetime = '20'+msg[37:38].hex()+'-'+msg[35:36].hex()+'-'+msg[36:37].hex()+' '+msg[32:33].hex()+':'+msg[33:34].hex()+':'+msg[34:35].hex()


        # Data text
        self.data = msg[38:-4].hex()

        # msg[38:-4].hex()


        # # CRCAES
        # self.__logHex(msg[-4:-2])

        # # CRC-16
        # self.__logHex(msg[-2:])

        # fullquery
        self.fullquery = msg.hex()


    def is_command_response(self):
        return self.messagetype == '1'

    def getResponse(self):
        return self.getResponseHead()

    def getResponseHead(self, is_command = False):

        #11 61 3a 00 2b 16 11 11 00 00 00 00 12 34 56 78 9a bc de f0 12 34 56 78 9a bc de f0 00 00 24 00 13 01 15 02 20 19 3b 0e 64 00 31 01 00 00 00 00 00 00 00 00 00 00 7f 00 00 00 00 00 ec 5b 90 99

        messagetype = b'\x10' if is_command else b'\x12'
        
        # datachannel - 1 байт – не расшифровывая лупишь туда весь байт, как есть (нолики, единички) varchar(8)
        datachannel = b'\x02' if is_command else b'\x00'
        
        #  sizebytes 
        body = self.getResponseBody(is_command)
        sizebytes = len(body).to_bytes(2, byteorder='little')

        log.info('sizebytes:')
        log.info(len(body))
        
        # crcHead
        head = messagetype + datachannel + sizebytes

        crcHead = self.__calcCRC(head)

        log.info('response:')
        self.__logHex(head + crcHead + body)

        return head + crcHead + body

    def getResponseIdent(self, is_command = False):
        # messageid int
        messageid = b'\x00\x00' if is_command else self.messageidByte

        log.info('messageid:')
        self.__logHex(messageid)

        # 8 байт – IMEI устройства управления
        imei = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        # 2 байта – Номер пользователя, если =0, то отсутствует
        userid = b'\x00\x00'
        # 2 байта – Случайное число – используется для выбора ключа шифрования. Если =0, то сообщение не зашифровано.
        key = b'\x00\x00'
                

        log.info('ident(14):')
        self.__logHex(messageid + imei + userid + key)
        return messageid + imei + userid + key

    def getResponseData(self, is_command = False):
        ### Data text ###
        data =  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' if is_command else self.commandByte + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        log.info('data(16):')
        self.__logHex(data)
        return data

    def getResponseBody(self, is_command = False):
        body = self.getResponseIdent(is_command) + self.getResponseData(is_command)
        bodyCRC = self.__calcCRC(body)
        return body + bodyCRC


    def __calcCRC(self, msg):
        crc16 = crcmod.mkCrcFun(0x1021, rev=False, initCrc=0x0000, xorOut=0x0000)
        return crc16(msg).to_bytes(2, byteorder='big')


    def __logHex(self, msg):
        log.info( " ".join(["{:02x}".format(x).upper() for x in msg]))
