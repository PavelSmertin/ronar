__author__ = 'Pashtet <pashtetbezd@gmail.com>'


from datetime import datetime
#from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, DateTime, select, desc

import pymysql.cursors
#from sshtunnel import SSHTunnelForwarder







class EventStore():

    def __init__(self):
      print('__init__')

    def close(self):
      print('close')

    def store_event(self, message):


      # with SSHTunnelForwarder(
      #   ('78.46.193.86', 22),
      #   ssh_username='root',
      #   ssh_password='akunamatata',
      #   remote_bind_address=('127.0.0.1', 3306),
      # ) as tunnel:
        connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            password='@kunamatat@',
                            db='signal',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

        try:
          with connection.cursor() as cursor:
              # Create a new record
              sql = "INSERT INTO `commandsincoming` (`messagetype`, `datachannel`, `sizebytes`, `messageid`, `device_iddevice`, `datetime`, `data`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
              #cursor.execute(sql, (message.messagetype, message.datachannel, message.sizebytes, message.messageid, message.device_iddevice, message.datetime, message.data))

          #print('store_event')
          #print(message.data)
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          connection.commit()

          # with connection.cursor() as cursor:
          #     # Read a single record
          #     sql = "SELECT * FROM `commandsincoming` WHERE `messageid`=%s"
          #     cursor.execute(sql, ('message.messageid',))
          #     result = cursor.fetchone()
          #     print(result)
        finally:
          connection.close()


