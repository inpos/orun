
import json
from . import js
import re

__all__ = ['create', 'createByAlias', 'Component']

def js_ajax(fn, arg_dict = {}):
    i = id(fn)
    js.live_methods[i] = fn
    func_args = ', '.join(['\'{k}\': {v}'.format( k = k,v = '\'%s\'' % v if type(v) is str else v  ) for k,v in arg_dict.items()])
    if func_args != '': func_args = ', ' + func_args
    return "%s({'url': '%s', 'method': 'GET', 'params': { 'fn': %d, 'id_': %s %s}, 'success': %s })"\
        % (js.client.Ext.Ajax.request, js.AJAX_URL, i, js.client.this.id, func_args, js.function('eval(arguments[0].responseText);'))

js.js_ajax = js_ajax

def _create(meth, name, args):
    #args['pyLive'] = True : TODO
    obj = Component(**args)
    js.write('var %s = Ext.create(\'%s\', %s);' % (obj._id, name, str(obj)))
    return obj

def create(name, args={}):
    return _create('create', name, args)

def createByAlias(alias, args={}):
    return _create('createByAlias', alias, args)

def get(id):
    return js.JsNode('Ext.get(\'%s\')' % id)

def getCmp(id):
    return js.JsNode('Ext.getCmp(\'%s\')' % id)
def getBody():
    return js.JsNode('Ext.getBody()')

class Component(js.JsObject):
    def __init__(self, *args, **kwargs):
        super(Component, self).__init__(*args, **kwargs)
        
    def _update(self, config):
        def get_obj(value):
            if isinstance(value, dict):
                return Component(**v)
            elif isinstance(value, (list, tuple)):
                return [get_obj(v) for v in value]
            else:
                return value
        cfg = {}
        for k, v in config.items():
            cfg[k] = get_obj(v)
        super(Component, self).update(cfg)
        
    def down(self, item):
        pass
    
    def up(self, item):
        pass
    
    def __str__(self):
        s = json.dumps(self._js, default=js._encoder, indent=4)
        return re.sub(r'("(handler|renderTo)":\s+)("([^"]+)")', r'\1\4', s)
