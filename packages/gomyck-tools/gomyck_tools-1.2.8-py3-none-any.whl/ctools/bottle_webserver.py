import sys
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

from bottle import ServerAdapter, Bottle, template, static_file, abort, redirect

from ctools import sys_info

"""
module_names = list(globals().keys())
def get_modules():
  mods = []
  for modname in module_names:
    if modname == 'base' or modname == 'online' or modname.startswith('__') or modname == 'importlib': continue
    module = globals()[modname]
    mods.append(module)
  return mods

def get_ws_modules():
  from . import websocket
  return [websocket]
"""

"""
from ctools import bottle_web_base, token, bottle_webserver
from ctools.api_result import R

secret_key = "xxx"
app = bottle_web_base.init_app('子模块写 context_path, 主模块就不用写任何东西')

# 通用的鉴权方法
@bottle_web_base.before_intercept(0)
def token_check():
  return bottle_web_base.common_auth_verify(secret_key)

@app.post('/login')
def login(params):
  return R.ok(token.gen_token({'username': 'xxx'}, secret_key, 3600))

@app.get('/demo')
@bottle_web_base.rule('DOC:DOWNLOAD')
def demo(params):
  print(params)

main_app = bottle_webserver.init_bottle() # 这里可以传 APP 当做主模块, 但是 context_path 就不好使了, 上下文必须是 /
main_app.mount(app.context_path, app)
main_app.set_index(r'轨迹点位压缩.html')
main_app.run()
"""

_default_port = 8888

class CBottle:

  def __init__(self, bottle: Bottle, port=_default_port, quiet=False):
    self.port = port
    self.quiet = quiet
    self.bottle = bottle

  def run(self):
    http_server = WSGIRefServer(port=self.port)
    print('Click the link below to open the service homepage %s' % '\n \t\t http://localhost:%s \n \t\t http://%s:%s' %  (self.port, sys_info.get_local_ipv4(), self.port), file=sys.stderr)
    self.bottle.run(server=http_server, quiet=self.quiet)

  def set_index(self, root='./', filename='index.html', is_tpl=False, redirect_url=None, **kwargs):
    @self.bottle.route(['/', '/index'])
    def index():
      try:
        if redirect_url: return redirect(redirect_url)
        if is_tpl: return template(f"{root}/{filename}", **kwargs)
        return static_file(filename=filename, root=root, **kwargs)
      except FileNotFoundError:
        abort(404, "File not found...")

  def set_static(self, root):
    @self.bottle.route('/static/<filepath:path>')
    def static(filepath):
      try:
        return static_file(filepath, root=root)
      except FileNotFoundError:
        abort(404, "File not found...")

  def set_download(self, root):
    @self.bottle.route('/download/<filepath:path>')
    def download(filepath):
      return static_file(filepath, root=root, download=True)

  def mount(self, context_path, app, **kwargs):
    self.bottle.mount(context_path, app, **kwargs)

def init_bottle(app:Bottle=None, port=_default_port, quiet=False) -> CBottle:
  bottle = app or Bottle()
  return CBottle(bottle, port, quiet)

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
  daemon_threads = True

class CustomWSGIHandler(WSGIRequestHandler):
  def log_request(*args, **kw): pass

class WSGIRefServer(ServerAdapter):

  def __init__(self, host='0.0.0.0', port=_default_port):
    super().__init__(host, port)
    self.server = None

  def run(self, handler):
    req_handler = WSGIRequestHandler
    if self.quiet: req_handler = CustomWSGIHandler
    self.server = make_server(self.host, self.port, handler, server_class=ThreadedWSGIServer, handler_class=req_handler)
    self.server.serve_forever()

  def stop(self):
    self.server.shutdown()
