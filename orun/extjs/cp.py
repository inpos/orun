
import os
from orun.extjs import *
from orun.servers import cp
import cherrypy

THEME = 'gray'

@cherrypy.expose
class ExtJS:
    _cp_config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.dirname(__file__), 'static','ext-4.2.1'),
        }

class ExtApplication(cp.Application):
    def __init__(self, title=''):
        super(ExtApplication, self).__init__(title)
        self.ext_421 = ExtJS()
    
    def index(self, *args, **kwargs):
        f = open(os.path.join(os.path.dirname(__file__), 'app.html')).read()
        self.main()
        return f % (self.title, THEME, THEME, str(js.js_manager))
    index.exposed = True
    
    def ajax_callback(self, *args, **kwargs):
        fn = kwargs.pop('fn')
        if fn:
            fn = js.live_methods[int(fn)]
            fn(*args, **kwargs)
        return str(js.js_manager)
    ajax_callback.exposed = True
    
if __name__ == '__main__':
    app = ExtApplication('Orun (ExtJS Application)')
    app.run()
