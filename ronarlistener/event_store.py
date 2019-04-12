__author__ = 'Pashtet <pashtetbezd@gmail.com>'


from datetime import datetime
#from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, DateTime, select, desc


import pymysql.cursors







class EventStore():

    def __init__(self):
      print('__init__')
        # self.engine = create_engine('sqlite:///sonar_events.db')
        # metadata = MetaData()
        # self.sonar_events = Table('ro_tem_events', metadata,
        #                           Column('id', Integer, primary_key=True),
        #                           Column('protocol', String(20), nullable=False),
        #                           Column('seq', String(4), nullable=False),
        #                           Column('rrcvr', String(7)),
        #                           Column('lpref', String(7), nullable=False),
        #                           Column('acct', String(17), nullable=False),
        #                           Column('data_type', String(1), nullable=False),
        #                           Column('data_code', String(3), nullable=False),
        #                           Column('data_sensor_number', String(2), nullable=False),
        #                           Column('data_sensor_value', String(8), nullable=False),
        #                           Column('data_gsm_level', String(2), nullable=False),
        #                           Column('timestamp', DateTime, nullable=False)
        #                           )
        # metadata.create_all(self.engine)

    def close(self):
      print('close')
        #self.engine.dispose()

    def store_event(self, message):

      connection = pymysql.connect(host='localhost',
                             user='root',
                             password='passwd',
                             db='signal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

      try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `comandsincoming` (`messagetype`, `datachannel`, `sizebytes`, `messageid`, `device_iddevice`, `datetime`, `data`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (message.messagetype, message.datachannel, message.sizebytes, message.messageid, message.device_iddevice, message.datetime, message.data))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `comandsincoming` WHERE `messageid`=%s"
            cursor.execute(sql, ('message.messageid',))
            result = cursor.fetchone()
            print(result)
      finally:
        connection.close()


