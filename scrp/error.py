'''
scrp.error - exceptions etc.
'''

class ShellError(Exception):
    '''Unhandled error during mock shell execution.'''
    def __init__(self, message, node):
        self.message = message
        self.node = node
