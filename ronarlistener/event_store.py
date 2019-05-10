__author__ = 'Pashtet <pashtetbezd@gmail.com>'

import logging
from datetime import datetime
#from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, DateTime, select, desc

import pymysql.cursors
#from sshtunnel import SSHTunnelForwarder
log = logging.getLogger(__name__)

class EventStore():

    def __init__(self):
      log.info('mysql init')
      try:
        self.connection = pymysql.connect(host='127.0.0.1',
                              port=3306,
                              user='root',
                              password='@kunamatat@',
                              db='signal',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
      except pymysql.Error as e:
        log.warn('Got error mysql {}'.format(e.args[0]), exc_info=error)



    def close(self):
      log.info('mysql close')
      connection.close()

    def store_event(self, message):
        # log.info(message.datetime)
        return

        if self.connection is None:
          return

        try:
          with self.connection.cursor() as cursor:
              # Create a new record
              sql = "INSERT INTO `commandsincoming` (`messagetype`, `datachannel`, `sizebytes`, `messageid`, `device_iddevice`, `commands`, `datetime`, `data`, `fullquery`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
              cursor.execute(sql, (message.messagetype, message.datachannel, message.sizebytes, message.messageid, message.device_iddevice, message.command, message.datetime, message.data, message.fullquery))

          #print('store_event')
          #print(message.data)
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          self.connection.commit()

          # with connection.cursor() as cursor:
          #     # Read a single record
          #     sql = "SELECT * FROM `commandsincoming` WHERE `messageid`=%s"
          #     cursor.execute(sql, ('message.messageid',))
          #     result = cursor.fetchone()
          #     print(result)
        except pymysql.Error as e:
          log.warn('Got error mysql {}'.format(e.args[0]), exc_info=error)
        except:
          log.warn("Unexpected error:", sys.exc_info()[0])
          raise



