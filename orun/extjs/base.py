from . import js


__all__ = ['create', 'createByAlias', 'Component']

def js_ajax(fn, arg_dict = {}, f_type=js.js_procedure):
    i = id(fn)
    js.live_methods[i] = fn
    func_args = ',\n'.join(['\'{k}\': {v}'.format( k = k,v = js.encode(v) ) for k,v in arg_dict.items()])
    if func_args != '': 
        func_args = ',\n' + func_args
    return f_type(i, ajax_args=func_args)

js.js_ajax = js_ajax

def _create(meth, name, args):
    #args['pyLive'] = True : TODO
    obj = Component(**args)
    js.write('var %s = Ext.create(\'%s\', %s);' % (obj._id, name, str(obj)))
    return obj

def create(name, args={}):
    return _create('create', name, args)

def define(name, args={}):
    js.write('Ext.define(\'%s\', %s);' % (name, js.encode(args)))

def createByAlias(alias, args={}):
    return _create('createByAlias', alias, args)

def get(id):
    return js.JsNode('Ext.get(\'%s\')' % id)

def getCmp(id):
    return js.JsNode('Ext.getCmp(\'%s\')' % id)
def getBody():
    return js.JsNode('Ext.getBody()')

tip = js.JsNode('Ext.tip')

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
        return js.dict2extjs(self._js)
