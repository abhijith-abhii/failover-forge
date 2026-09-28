from pathlib import Path
import json
ROOT=Path(__file__).parent
def analyze(p):
 path=ROOT/'reports/recovery.json'
 if not path.exists():raise ValueError('No experiment evidence yet. Run python demo.py.')
 d=json.loads(path.read_text());return dict(metrics={'Measured failover':str(d['failover_ms'])+' ms','Restart to ready':str(d['restart_to_ready_ms'])+' ms','Environment':'same-host processes'},rows=d['events'],notice='One measured local run. Timing depends on this machine and is not an SLA or a cloud benchmark.',details=d)
