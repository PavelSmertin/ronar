__author__ = 'Pashtet <pashtetbezd@gmail.com>'


from datetime import datetime
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, DateTime, select, desc



class EventStore():

    def __init__(self):
        self.engine = create_engine('sqlite:///sonar_events.db')
        metadata = MetaData()
        self.sonar_events = Table('ro_tem_events', metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('protocol', String(20), nullable=False),
                                  Column('seq', String(4), nullable=False),
                                  Column('rrcvr', String(7)),
                                  Column('lpref', String(7), nullable=False),
                                  Column('acct', String(17), nullable=False),
                                  Column('data_type', String(1), nullable=False),
                                  Column('data_code', String(3), nullable=False),
                                  Column('data_sensor_number', String(2), nullable=False),
                                  Column('data_sensor_value', String(8), nullable=False),
                                  Column('data_gsm_level', String(2), nullable=False),
                                  Column('timestamp', DateTime, nullable=False)
                                  )
        metadata.create_all(self.engine)

    def close(self):
        self.engine.dispose()

    def store_event(self, message):
        with self.engine.begin() as connection:
            result = connection.execute(self.sonar_events.insert(), 
                                            protocol = message.protocol_in, 
                                            seq = message.seq, 
                                            rrcvr = message.rrcvr, 
                                            lpref = message.lpref, 
                                            acct = message.acct, 
                                            data_type = message.data_type, 
                                            data_code = message.data_code, 
                                            data_sensor_number = message.data_sensor_number, 
                                            data_sensor_value = message.data_sensor_value, 
                                            data_gsm_level = message.data_gsm_level, 
                                            timestamp = datetime.strptime(message.msg_timestamp, "%H:%M:%S,%m-%d-%Y")
                                        )
