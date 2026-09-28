"""Real local-process fault injection; no cloud resources."""
import subprocess,sys,os,time,json,socket,urllib.request
from pathlib import Path
ROOT=Path(__file__).parent

def available_port():
 with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def probe(port):
 with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=.2) as r:return json.load(r)
def start(port,name):
 p=subprocess.Popen([sys.executable,str(ROOT/'service.py'),str(port)],env={**os.environ,'NODE_NAME':name},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 for _ in range(50):
  try:probe(port);return p
  except OSError:time.sleep(.02)
 p.terminate();p.wait();raise RuntimeError('Node failed readiness')
def request_with_failover(primary,secondary):
 errors=[]
 for port in [primary,secondary]:
  try:return probe(port),errors
  except OSError as e:errors.append(type(e).__name__)
 raise RuntimeError('Both nodes unavailable')
def run():
 primary,secondary=available_port(),available_port();p=s=None;events=[]
 try:
  p=start(primary,'primary');s=start(secondary,'secondary')
  before,_=request_with_failover(primary,secondary);assert before['node']=='primary';events.append({'phase':'healthy','served_by':'primary'})
  p.terminate();p.wait(timeout=3);start_time=time.perf_counter();after,errors=request_with_failover(primary,secondary);failover_ms=(time.perf_counter()-start_time)*1000
  assert after['node']=='secondary' and errors;events.append({'phase':'primary terminated','served_by':'secondary','primary_error':errors[0]})
  recovery_start=time.perf_counter();p=start(primary,'primary');recovered,_=request_with_failover(primary,secondary);recovery_ms=(time.perf_counter()-recovery_start)*1000;assert recovered['node']=='primary';events.append({'phase':'primary restarted','served_by':'primary'})
  report={'mode':'local HTTP process experiment','failover_ms':round(failover_ms,3),'restart_to_ready_ms':round(recovery_ms,3),'events':events,'request_attempts':3,'data_loss':'not measured; service is stateless','rpo':'not applicable','topology':'same host; sequential client-side fallback; not a proxy or multi-region system'}
  (ROOT/'reports').mkdir(exist_ok=True);(ROOT/'reports/recovery.json').write_text(json.dumps(report,indent=2));return report
 finally:
  for process in [p,s]:
   if process and process.poll() is None:process.terminate();process.wait(timeout=3)
if __name__=='__main__':print(json.dumps(run(),indent=2))
