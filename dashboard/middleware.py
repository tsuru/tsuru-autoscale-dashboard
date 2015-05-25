import logging
import traceback
import sys
from django.http import Http404


class LogMiddleware(object):

    def process_exception(self, request, exception):
        exc_info = sys.exc_info()

        if not isinstance(exception, Http404):
            logging.error("######################## Exception #############################")
            logging.error('\n'.join(traceback.format_exception(*(exc_info or sys.exc_info()))))
            logging.error("################################################################")
