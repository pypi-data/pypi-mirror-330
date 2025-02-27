#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File    :   can_func.py
@Time    :   2025/2/18 9:55
@Author  :   CLZMFQ
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This package realizes functionality of sending can message
'''

from simpleCan.util import xldriver, dataStructure as ds
import logging, ctypes, time

def sendMessage(messageID, data, messageCount=1):
    canID = ds.XL_CAN_EXT_MSG_ID | messageID
    myXLevent = (ds.XLevent * messageCount)()
    message_count = ctypes.c_uint(messageCount)
    try:
        xldriver.libc.memset(myXLevent, 0, ctypes.sizeof(myXLevent))
        for i in range(messageCount):
            myXLevent[i].tag = xldriver.XLeventTag_transmit
            myXLevent[i].tagData.msg.id = canID
            myXLevent[i].tagData.msg.flags = xldriver.flags
            for j in range(len(data)):
                myXLevent[i].tagData.msg.data[j] = data[j]
            myXLevent[i].tagData.msg.dlc = xldriver.dlc
        result = xldriver.xlCanTransmit(xldriver.portHandle, channelMask, message_count, myXLevent)
        if result == 0:
            logging.info('send message ' + str(hex(messageID)) + ' result ' + str(result))
        else:
            logging.error('send message ' + str(hex(messageID)) + ' result ' + str(result))
    except Exception as e:
        logging.error(f"Error: {e}")

def recvMessage() -> ds.ReceivedCanMessage:
    xLevent = ds.XLevent()
    pxLevent = ctypes.pointer(xLevent)
    pEventCount = ctypes.pointer(ctypes.c_uint(1))
    xlstatus = xldriver.xlReceive(xldriver.portHandle, pEventCount, pxLevent)
    timeStamp = time.time()
    if xlstatus == 0:
        msgID = xLevent.tagData.msg.id & 0x1FFFFFFF
        msgData = list(xLevent.tagData.msg.data)
        systemTimeStamp = xLevent.timeStamp
        logging.critical(
            'received message ' + str(hex(msgID)) + ' timestamp ' + str(timeStamp) + ' system time ' + str(systemTimeStamp))
        return ds.ReceivedCanMessage(message_id=msgID, data=msgData, timestamp=timeStamp,
                                     systemTimeStamp=systemTimeStamp)

def getSyncTime():
    xlstatus = xldriver.xlGetSyncTime(xldriver.portHandle, xldriver.pTime)
    logging.info('xl get sync time result is ' + str(xlstatus))
    return xldriver.time


def setup():
    xlstatus = xldriver.xlOpenDriver()
    logging.critical('open driver result is ' + str(xlstatus))

    xlstatus = xldriver.xlGetDriverConfig(xldriver.pxldriverConfig)
    logging.critical('get driver config result is ' + str(xlstatus))
    logging.critical('channelIndex value is ' + str(hex(xldriver.xldriverConfig.channel[0].channelIndex)))
    logging.critical('channelMask value is ' + str(hex(xldriver.xldriverConfig.channel[0].channelMask)))
    logging.critical('channelCapabilities value is ' + str(hex(xldriver.xldriverConfig.channel[0].channelCapabilities)))
    logging.critical(
        'channelBusCapabilities value is ' + str(hex(xldriver.xldriverConfig.channel[0].channelBusCapabilities)))

    xlstatus = xldriver.xlGetApplConfig(xldriver.pAppName, xldriver.appChannel, xldriver.pHwType, xldriver.pHwIndex,
                                        xldriver.pHwChannel, xldriver.busTypex)
    logging.critical('get appl config result is ' + str(xlstatus))
    logging.critical('hardware type is ' + ds.get_hwtype_name(xldriver.HwType.value))

    global channelMask
    channelMask = xldriver.xlGetChannelMask(xldriver.HwType, xldriver.HwIndex, xldriver.HwChannel)
    logging.critical('channel mask is %d', channelMask)

    xlstatus = xldriver.xlOpenPort(xldriver.pPortHandle,
                                   xldriver.userName,
                                   channelMask,
                                   xldriver.pPermissionMask,
                                   xldriver.rx_queue_size,
                                   xldriver.xlInterfaceVersion,
                                   xldriver.busType)
    logging.critical('port handler value is ' + str(xldriver.portHandle))
    assert xlstatus != -1
    logging.critical('open port result is ' + str(xlstatus))
    xlstatus = xldriver.xlActivateChannel(xldriver.portHandle,
                                          channelMask,
                                          xldriver.busType,
                                          xldriver.activate_channel_flag)
    logging.critical('Activate channel result is ' + str(xlstatus))

    xlstatus = xldriver.xlResetClock(xldriver.portHandle)

    logging.critical('xl reset clock result is ' + str(xlstatus))

def teardown():
    xlstatus = xldriver.xlDeactivateChannel(xldriver.portHandle, channelMask)
    logging.critical('deactivate channel result is ' + str(xlstatus))

    xlstatus = xldriver.xlClosePort(xldriver.portHandle)
    logging.critical('close port result is ' + str(xlstatus))

    xlstatus = xldriver.xlCloseDriver()
    logging.critical('close driver result is ' + str(xlstatus))
