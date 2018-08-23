
import os
from orun.extjs import *
from orun.servers import cp
import cherrypy

THEME_MODEL = 'classic'
THEME = 'gray'
CHART_THEME_MODEL = 'classic/classic' if THEME_MODEL == 'classic' else 'modern/modern-' + THEME
BASE_URL = ''
ENABLE_CHARTS=False

@cherrypy.expose
class ExtJS:
    _cp_config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.dirname(__file__), 'static','ext-6.2.0'),
        }

class ExtApplication(cp.Application):
    def __init__(self, title=''):
        super(ExtApplication, self).__init__(title)
        self.ext_620 = ExtJS()
    
    @cherrypy.expose
    def index(self, *args, **kwargs):
        f = open(os.path.join(os.path.dirname(__file__), 'app.html')).read()
        self.main()
        
        CHART_HTML_CODE = '''<script type="text/javascript" src="{base_url}/ext_620/packages/charts/{theme_model}/charts.js"></script>
    <link rel="stylesheet" type="text/css" href="{base_url}/ext_620/packages/charts/{chart_theme_model}/resources/charts-all.css">
'''.format(base_url=BASE_URL,
            theme_model=THEME_MODEL,
            chart_theme_model=CHART_THEME_MODEL)
        EXTJS_PACKAGES = '' + CHART_HTML_CODE if ENABLE_CHARTS else ''
        
        return f.format(title=self.title,
                        base_url=BASE_URL,
                        theme=THEME,
                        theme_model=THEME_MODEL,
                        script=str(js.js_manager),
                        packages=EXTJS_PACKAGES)
    
    @cherrypy.expose
    def ajax_callback(self, *args, **kwargs):
        fn = kwargs.pop('fn')
        if fn:
            fn = js.live_methods[int(fn)].func
            fn(*args, **kwargs)
        return str(js.js_manager)
    
    @cherrypy.expose
    @cp.cherrypy.tools.json_out()
    def ajax_func_callback(self, *args, **kwargs):
        fn = kwargs.pop('fn')
        if fn:
            fn = js.live_methods[int(fn)].func
            res = fn(*args, **kwargs)
            return {
                'data': res
                }
        else:
            return {
                'data': None
                }
    
if __name__ == '__main__':
    app = ExtApplication('Orun (ExtJS Application)')
    app.run()
