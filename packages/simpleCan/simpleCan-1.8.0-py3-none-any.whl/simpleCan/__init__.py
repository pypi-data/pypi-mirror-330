import logging
from simpleCan.util import dataStructure as ds, can_func, dbcReader
from simpleCan.util.task import SendMessageTask, RecvMessageTask
from simpleCan.util.messageList import MessageList

__all__ = ['SimpleCan']


class SimpleCan:

    def __init__(self, dbcPath):
        # create a list to store all messages sending to DDU
        self.tasklist = []
        self.messageList = MessageList()
        self.dbcReader = dbcReader.DBCReader(dbcPath=dbcPath)
        can_func.setup()

    def env_setupAndRun(self, duration=360):
        self.messageList.clearMessageList()
        self.messageList.load_default_messageList()
        messageList = self.messageList.get_messageList()
        self.clearTaskList()
        for i in range(len(messageList)):
            self.tasklist.append(SendMessageTask(message_id=messageList[i].id,
                                                 data=messageList[i].data,
                                                 period=messageList[i].period,
                                                 duration=duration))
        self.env_run()
    def env_run(self):
        for task in self.tasklist:
            task.task_run()

    def sendAllMessagesFromDBC(self, duration = 30):
        canTxMessageList = self.dbcReader.getcanTxMessageList()
        for canMessage in canTxMessageList:
            self.sendMessage(message_id=canMessage.id, period = canMessage.period, data=canMessage.data, duration = duration)


    def sendCanMessage(self, message, duration = 30, **kwargs):
        canMessage = self.dbcReader.generateCanMessage(message = message, duration = duration, **kwargs)
        self.sendMessage(message_id=canMessage.id, data = canMessage.data, period = canMessage.period, duration=duration)


    def sendMessage(self, message_id, data, period, duration=30):
        task = SendMessageTask(message_id=message_id,
                               data=data,
                               period=period,
                               duration=duration)
        self.tasklist.append(task)
        task.task_run()


    def recvMessage(self):
        return RecvMessageTask.recvMessage()

    def recvTargetMessage(self, message_id, offset = 0, duration=10) -> ds.ReceivedCanMessage:
        return RecvMessageTask.recvTargetMessage(message_id=message_id, offset = offset, duration = duration)

    def modifyMessage(self, message_id, data):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    logging.critical(task.get_messageID())
                    task.task_modifyData(newData=data)

        except Exception as e:
            logging.error(e)

    def stopMessage(self, message_id):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    task.task_stop()
        except Exception as e:
            logging.error(e)

    def clearTaskList(self):
        self.tasklist = []

    def endAllTasks(self):
        for task in self.tasklist:
            task.task_stop()

    def __del__(self):
        self.endAllTasks()
        can_func.teardown()
