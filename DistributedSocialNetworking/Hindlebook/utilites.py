import logging
import traceback
import pprint
import json
from django.core import serializers

"""
 Prints out debug information including
 file and line number with log messages.
 
 Usage Example:
 
 from Hindlebook.utilites import Logger
 logger = Logger()
 
 # log a simple message
 logger.log("test")
 
 # log a stack trace (default 5 depth)
 logger.trace()
 
 # log an object
 logger.obj(obj)
"""

class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger('custom')
    
    # logs a string message to log.txt
    def log(self, message):
        try:
            file_name = traceback.extract_stack(limit=2)[0][0].split("DistributedSocialNetworking/", 1)[1]
            line = traceback.extract_stack(limit=2)[0][1]
            trace = "\n\n" + "    line: " + str(line) + " in " + file_name + "\n"
            self.logger.debug(trace + "    Message: " + message + "\n")
        except:
            self.logger.debug("\n\n Error while logging message.\n")
        
    # logs the current stack trace minus this call to log.txt
    def trace(self, limit=5):
        try:
            trace = '\n    '.join(traceback.format_list(traceback.extract_stack(limit=6)[0:5]))
            self.logger.debug("\n\n    " + trace)
        except:
            self.logger.debug("\n\n Error while logging stack trace.\n")
        
    # logs an object as json to log.txt
    def obj(self, obj):
        try:
            file_name = traceback.extract_stack(limit=2)[0][0].split("DistributedSocialNetworking/", 1)[1]
            line = traceback.extract_stack(limit=2)[0][1]
            trace = "\n\n" + "    line: " + str(line) + " in " + file_name + "\n"
            
            if obj is None:
                obj_class = None
                pretty_json = "(None)"
            else:
                obj_class = obj.__class__.__name__ 
                obj_json = serializers.serialize('json', [ obj, ])
                pretty_json = pprint.pformat(json.loads(obj_json))
            self.logger.debug(trace + "    Object: " + obj_class + "\n    " + pretty_json + "\n")
        except:
            self.logger.debug("\n\n Error while logging object.\n")
