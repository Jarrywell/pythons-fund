#!/usr/bin/python

import datetime
import os

_LOG_FILE = None
_verbose = False
_log_time = True


def Init(log_file_path):
    '''
    set the path to the log file
    :param log_file_path: 
    :return: 
    '''
    global _LOG_FILE
    _LOG_FILE = log_file_path;

    print 'Using log file: %s' % _LOG_FILE

def GetLogFilePath():
    '''
    return the path and name of the Log file
    :return: 
    '''

    global _LOG_FILE
    return _LOG_FILE

def Log(tag, msg):
    '''
    appends msg to the end of _LOG_FILE and prints it to sdtout
    :param msg: 
    :return: 
    '''
    log_string = _PrependTimeStamp(tag, msg)
    print log_string

    _WriteLog(log_string)


def SlientLog(tag, msg):
    '''
     sliently log msg. Unless verbose mode is enabled, will log msg only to the log file
    :param msg: 
    :return: 
    '''
    global _verbose

    log_string = _PrependTimeStamp(tag, msg)

    if _verbose:
        print _verbose

    _WriteLog(log_string)

def _WriteLog(msg):
    global _LOG_FILE
    if _LOG_FILE is not None:
        file_handler = open(_LOG_FILE, 'a')
        file_handler.write('\n' + str(msg))
        file_handler.close()

def _PrependTimeStamp(tag, msg):
    '''
    return the msg prepended with current timestamp
    :param tag:
    :param msg: 
    :return: 
    '''
    global _log_time
    if _log_time:
        return "[%s] %s: %s" % (datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S"), tag, msg)
    else:
        return msg

def setVerbose(_verbose_value=True):
    global _verbose
    _verbose = _verbose_value

def setTimestampLogging(_timestamp=True):
    global _log_time
    _log_time = _timestamp

_TAG = "Test"
def main():
    #pass
    log_path = os.getcwd()
    Init(os.path.join(log_path, 'test-log.txt'))
    Log(_TAG, 'this is Jarry test log')

if __name__ == '__main__':
    main()

