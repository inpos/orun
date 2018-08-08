from orun.extjs import *
from orun.extjs import cp

def ok_click(id_, *args, **kwargs):
    js.cli << Ext.getCmp(id_).setText('Clicked')
    js.cli << js.client.alert('Server side message')

def button_click(id_, *args, **kwargs):
    js.write("""
    Ext.getCmp("%s").setText('Clicked');
    alert('Server side callback message');
    """ % id_)

class MyApplication(cp.ExtApplication):
    def main(self, *args, **kwargs):
        wnd = Ext.create('widget.window', {'title': 'My Window', 'width': 300, 'height': 250,
            'items': [{'xtype': 'button', 'text': 'Click Here', 'handler': button_click}],
            'buttons': [
                {'text': 'OK', 'handler': js.FuncWithParams(ok_click, {'arg1': 1, 'arg2': 'val2', 'arg3': js.cli.this.id})},
                {'text': 'Close', 'handler': js.function('this.up(\'window\').close()')}]})
        wnd.show()
        wnd.setHeight(200)

cp.THEME = 'classic'

app = MyApplication('Orun (ExtJS Application)')
app.run()
