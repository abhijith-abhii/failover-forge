from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import sys,json,os
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  body=json.dumps({'node':os.environ.get('NODE_NAME','node'),'status':'ok'}).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)
 def log_message(self,*args):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(sys.argv[1])),Handler).serve_forever()
