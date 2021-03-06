import json

AJAX_URL = '/ajax_callback'
AJAX_FUNC_URL = '/ajax_func_callback'
js_manager = None
js_ajax = None

live_methods = {}

class RE:
    def __init__(self, re):
        self.re = re

def re(pattern):
    return RE(pattern)

def js_procedure(func_id, ajax_args=''):
    return '''
    Ext.Ajax.request(
        {
            url: '%s',
            method: 'GET',
            params: {
                        fn: %d%s
                },
            success: function () { eval(arguments[0].responseText); }
        }
    );
''' % (
        AJAX_URL,
        func_id,
        ajax_args
    )

def js_function(func_id, ajax_args=''):
    return '''
    var response = Ext.Ajax.request(
        {
            url: '%s',
            method: 'GET',
            async: false,
            params: {
                        fn: %d%s
            },
        }
    );
    var ajax_result = JSON.parse(response.responseText);
    return ajax_result.data;
''' % (
        AJAX_FUNC_URL,
        func_id,
        ajax_args
    )

def list2extjs(l):
    return '[ %s ]' % ', '.join([encode(v) for v in l])

def dict2extjs(d):
    return '{ %s }' % ', '.join('%s: %s' % (k, encode(v)) for k,v in d.items())

class JsProcedure:
    def __init__(self, *a, **kw):
        self.func = a[0]
        self.params = kw.get('params', {})
        self.args = kw.get('args', [])
    @property
    def js(self):
        return 'function (%s) { %s }' % (', '.join(self.args), js_ajax(self, arg_dict=self.params, f_type=js_procedure))

class JsFunction(JsProcedure):
    @property
    def js(self):
        return 'function (%s) { %s }' % (', '.join(self.args), js_ajax(self, arg_dict=self.params, f_type=js_function))

class JsStrFunction:
    def __init__(self, *a, **kw):
        self.code = a[0]
        self.args = kw.get('args', [])
    @property
    def js(self):
        return 'function (%s) { %s }' % (', '.join(self.args), self.code)

function = JsFunction
procedure = JsProcedure
strfunction = JsStrFunction
    
def encode(o):
    if isinstance(o, JsNode):
        return str(o)
    if isinstance(o, RE):
        return o.re
    elif isinstance(o, (list, tuple)):
        return list2extjs(o)
    elif isinstance(o, bool):
        return str(o).lower()
    elif isinstance(o, int):
        return str(o)
    elif isinstance(o, float):
        return str(o)
    elif isinstance(o, str):
        return '\'%s\'' % o
    elif isinstance(o, (function, procedure, strfunction)):
        return o.js
    elif isinstance(o, dict):
        return dict2extjs(o)
    elif isinstance(o, JsObject):
        return o._id
    else:
        return str(o)

class JsBlock:
    def __init__(self, *args, **kwargs):
        self.code = args[0]
        self.args = args[1] if len(args) > 1 else []
        
    def __str__(self):
        return self.code
    
def write(code):
    if js_manager:
        js_manager.write(str(code))
        
    def __lshift__(self, value):
        print('test')

class JsManager(object):
    def __init__(self):
        self.output = []
    
    def write(self, data):
        self.output.append(data)
        
    def __str__(self):
        output = self.output[:]
        s = '\n'.join(output)
        
        return s
    
class JsNode(object):
    def __init__(self, name='', parent=None):
        if parent and parent.name:
            self.name = parent.name + '.' + name
        else:
            self.name = name

    def __getattr__(self, attr):
        return JsNode(attr, self)
    
    def __setattr__(self, attr, value):
        if attr == 'name':
            super(JsNode, self).__setattr__(attr, value)
        else:
            value = encode(value)
            if self is client.var:
                s = 'var %s = %s' % (attr, value)
            else:
                name = self.name + '.' if self.name else ''
                s = '%s%s = %s' % (name, attr, value)
            write(s)
            
    def __add__(self, other):
        return JsNode('%s + %s' % (encode(self), encode(other)))

    def __sub__(self, other):
        return JsNode('%s - %s' % (encode(self), encode(other)))

    def __mul__(self, other):
        return JsNode('%s * %s' % (encode(self), encode(other)))

    def __truediv__(self, other):
        return JsNode('%s / %s' % (encode(self), encode(other)))

    def __call__(self, *args, **kwargs):
        l = []
        d = []
        for arg in args:
            l.append(encode(arg))
        for k, v in kwargs.items():
            d.append('%s=%s' % (k, encode(v)))
        _args = []
        if l:
            _args.extend(l)
        if d:
            _args.extend(d)
        s = '%s(%s)' % (self.name, ','.join(_args))
        self.name = s
        return self
    
    def __str__(self):
        return self.name
    
class JsClient(JsNode):
    def __init__(self, name='', parent=None):
        if parent and parent.name:
            self.name = parent.name + '.' + name
        else:
            self.name = name
        self.__dict__['var'] = JsNode('var')
        
    def __lshift__(self, other):
        write(other)
        
class JsObjectNode(JsNode):
    def __call__(self, *args, **kwargs):
        super(JsObjectNode, self).__call__(*args, **kwargs)
        write(str(self))

class JsOutput(object):
    def __init__(self, manager=True):
        self.body = []
        if manager:
            js_manager = self
        
    def __lshift__(self, other):
        self.write(other)
        
    def write(self, code):
        self.body.append(code)
        
    def __str__(self):
        s = ';\n'.join(self.body)
        return s
    
out = output = JsOutput

class JsObject(object):
    def __init__(self, *args, **kwargs):
        self._loading = True
        self._id = 'js_%s' % id(self)
        self._create()
        self._js = kwargs
        self._loading = False
        
    def _create(self):
        pass
    
    def _update(self, config):
        self._js.update(config)

    def __getattr__(self, attr):
        if not self.__dict__.get('_loading', True):
            if attr in self._js:
                return self._js.get(attr)
            else:
                return JsObjectNode(attr, JsNode(self._id))
    
    def __setattr__(self, attr, value):
        if '_js' in self.__dict__ and not attr in self.__dict__:
            self[attr] = value
        else:
            super(JsObject, self).__setattr__(attr, value)
        
    def __setitem__(self, attr, value):
        if not self._loading:
            write('%s.%s = %s' % (self._id, attr, json.dumps(value)))
        self._js[attr] = value
        
def alert(msg):
    write(client.alert(msg))

def load(filename, klass=JsObject):
    return klass(**json.load(open(filename)))

cli = client = JsClient()

if __name__ == '__main__':
    class MyManager(JsManager):
        def write(self, code):
            print(code)
    js_manager = MyManager()
    write(client.console.log('test'))
    n = JsNode('console')
    write(n.print(n.log({'id': 'item id'})))
    client.var.x = 1
    client.x.y = client.window.open('http://www.google.com')
    client << client.x.y()([client.x])
    client << client.Ext.create('window', {'left': 10})
    client << client.x
    
    # test block
    print(encode({'click': 'call'}))
