import logging


class SystemLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'info'):
            record.info = '{}'
        return True
