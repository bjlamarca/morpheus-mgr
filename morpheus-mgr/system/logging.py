from pathlib import Path
import json, datetime, os
from datetime import datetime




BASE_DIR = str(Path(__file__).resolve().parent.parent)
         

LOG_LEVEL = (
        'VERBOSE',
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL',
    )

class SystemLogger():
    
    def __init__(self, module):
        self.logitem = {}
        self.logitem['module'] = module
        self.logitem['method'] = ''
        self.logitem['message'] = ''
        self.logitem['details'] = ''
        self.logitem['level'] = ''

    def log(self, method, message, details, level):
        #from system.models import SystemLog
        self.logitem['method'] = method
        self.logitem['message'] = message
        self.logitem['details'] = details
        self.logitem['level'] = level

        #write to file log and database
        #if DB write fails, log additional msg in file
    
        f = open(BASE_DIR + '/systemlog.log', 'a')
        self.logitem['date_time'] = str(datetime.now())
        log_json = json.dumps(self.logitem, indent=2) 
        f.write(log_json + ',\n')
        f.close

        # try:
        #     new_log = SystemLog()
        #     new_log.date_time = str(datetime.now())
        #     new_log.module = self.logitem['module']
        #     new_log.method = self.logitem['method']
        #     new_log.message = self.logitem['message']
        #     new_log.details = self.logitem['details']
        #     new_log.level = self.logitem['level']
        #     new_log.save()

        # except Exception as error:
        #     f = open('systemlog.log', 'a')
        #     self.logitem['date_time'] = str(datetime.now())
        #     self.logitem['message'] = 'Unable to write error to DB'
        #     self.logitem['details'] = str(error)
        #     self.logitem['level'] = 'WARNING' 
        #     log_json = json.dumps(self.logitem, indent=2) 
        #     f.write(log_json + ',\n')
        #     f.close       




