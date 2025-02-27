#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File    :   dbcReader.py
@Time    :   2025/2/26 9:58
@Author  :   CLZMFQ
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This package realizes functionality of sending can message
'''

import cantools, logging
from simpleCan.util import dataStructure as ds


class DBCReader:

    def __init__(self, dbcPath):
        self.databaseCan = None
        self.dbcPath = dbcPath
        self.canTxMessageList = []
        try:
            self.loadDBC()
            self.loadAllTxMessage()
        except Exception as e:
            logging.error(e)

    def loadDBC(self):
        if self.dbcPath is not None:
            try:
                self.databaseCan = cantools.database.load_file(self.dbcPath)
            except Exception as e:
                logging.error(f"Read DBC error: {e}")

    def loadAllTxMessage(self):
        try:
            for message in self.databaseCan.messages:
                if message.cycle_time is not None:
                    self.canTxMessageList.append(
                        ds.CanMessage(id=message.frame_id, data=[1, 3, 5], period=message.cycle_time / 1000))
        except Exception as e:
            logging.error(e)

    def generateCanMessage(self, message, duration=30, **kwargs) -> ds.CanMessage:
        try:
            message_from_dbc = self.databaseCan.get_message_by_name(message)
            id = message_from_dbc.frame_id
            period = message_from_dbc.cycle_time / 1000
            target_data = {}
            for signal in message_from_dbc.signals:
                if signal.name in kwargs:  # kwargs为字典格式
                    target_data[signal.name] = kwargs[signal.name]
                else:  # get message data from dbc
                    target_data[signal.name] = signal.raw_initial
            data = message_from_dbc.encode(target_data)
            return ds.CanMessage(id=id, data=data, period=period,
                                 duration=duration)

        except Exception as e:
            logging.error(f"Load can message error: {e}")

    def getcanTxMessageList(self):
        return self.canTxMessageList



