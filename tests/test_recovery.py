from demo import run

def test_real_failover_and_recovery():
 r=run();assert [x['served_by'] for x in r['events']]==['primary','secondary','primary']
 assert r['failover_ms']>=0 and r['restart_to_ready_ms']>=0
