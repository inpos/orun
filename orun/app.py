
from orun import js

class Application(object):
    AJAX_URL = '/ajax_callback'
    
    def __init__(self, title=''):
        self.title = title
        
    def main(self):
        pass
    
    def run(self):
        js.AJAX_URL = self.AJAX_URL
