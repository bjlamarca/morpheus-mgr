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
        self.logitem['method'] = method
        self.logitem['message'] = message
        self.logitem['details'] = details
        self.logitem['level'] = level
   
        f = open(BASE_DIR + '/systemlog.log', 'a')
        self.logitem['date_time'] = str(datetime.now())
        log_json = json.dumps(self.logitem, indent=2) 
        f.write(log_json + ',\n')
        f.close

        



