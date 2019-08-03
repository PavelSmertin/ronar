import crcmod
import logging
import datetime

log = logging.getLogger(__name__)


class Incoming():

    def __init__(self, msg = None):

        self._is_valid = False

        if msg == None: 
            log.info("was None")
            return

        if msg == 'S':
            log.info("was S")
            return

        if msg == b'\x53':
            log.info("was 0x53")
            return

        if len(msg) < 16: 
            log.info("was shorter 16")
            return

        if not isinstance(msg, bytes):
            log.info("was not bytes")
            return

        self._is_valid = True

        log.info("Imcoming message: ")
        log.info(msg)
        log.info("Channel: ")
        log.info(msg[1:2])


        self._msg = msg

        # Head - 6 байт
        self._message_type = msg[0:1]
        self._channel = "{0:08b}".format(int(msg[1:2].hex(), 16))
        self._size = int.from_bytes(msg[2:4], byteorder='little')
        self._crc_head = msg[4:6]

        # Identities - 24 байта (передается в открытом виде)
        self._message_id = msg[6:8]
        self._device_id = msg[8:12]

        # Data
        self._command = msg[30:32]
        self._datetime = '20'+msg[37:38].hex()+'-'+msg[35:36].hex()+'-'+msg[36:37].hex()+' '+msg[32:33].hex()+':'+msg[33:34].hex()+':'+msg[34:35].hex()
        self._data = msg[38:-4]
        self._crc_aes = msg[-4:-2]
        self._crc16 = msg[-2:]

    def is_valid(self):
        return self._is_valid

    def get_message_id(self):
        return self._message_id

    def get_id_from_tag(self, tag):
        return tag.to_bytes(2, byteorder='little')

    def is_response(self):
        return self._message_type == b'\x13'

    def get_event(self):
        return False if self._command[0:1] == b'\x24' else " ".join(["{:02x}".format(x).upper() for x in self._command])

    def get_response(self):
        return self.get_response_from(
            message_id      = self._message_id,
            message_type    = b'\x12',
            command         = self._command, 
            options         = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            )

    def get_response_from(self, message_id, message_type, command, options):
        data = Data(
            command = command,
            options = options
            )
        ident = Ident(
            message_id = message_id,
            imei = b'\x00\x00\x00\x00\x00\x00\x00\x00',
            user_id = b'\x00\x00',
            key = b'\x00\x00'
            )
        head = self.__get_head(
            data,
            ident,
            message_type    = message_type,
            channel         = b'\x00'
            )

        return head.get_message() + ident.get_message() + data.get_message() + head.get_body_crc()

    def __get_head(self, data, ident, message_type, channel):
        body = ident.get_message() + data.get_message()
        body_crc = self.__calcCRC(body)
        body_size = len(body + body_crc).to_bytes(2, byteorder='little')
        transport = message_type + channel + body_size
        head_crc = transport + self.__calcCRC(transport)

        return Head(
            head_crc        = head_crc,
            body_crc        = body_crc
            )

    def __calcCRC(self, msg):
        crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
        return crc16(msg).to_bytes(2, byteorder='big')

    def __logHex(self, msg):
        log.info( " ".join(["{:02x}".format(x).upper() for x in msg]))


class Head():
    def __init__(self, head_crc, body_crc):
        self._head_crc      = head_crc
        self._body_crc      = body_crc

    def get_message(self):
        return self._head_crc

    def get_body_crc(self):
        return self._body_crc

class Ident():
    def __init__(self, message_id, imei, user_id, key):
        self._message_id    = message_id
        self._imei          = imei
        self._user_id       = user_id
        self._key           = key

    def get_message(self):
        return self._message_id + self._imei + self._user_id + self._key

class Data():
    def __init__(self, command, options):
        self._command       = command
        self._options       = options

    def get_message(self):
        return self._command + self.__fill_data()

    def __fill_data(self):
        current_time        = datetime.datetime.now()
        current_time_str    = current_time.strftime("%H %M %S %m %d %y")
        current_time_bytes  = bytes.fromhex(current_time_str)
        return current_time_bytes + b'\x00\x00\x00\x00\x00\x00\x00\x00'
