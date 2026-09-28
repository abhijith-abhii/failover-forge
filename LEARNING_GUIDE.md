# Failover Forge — learning guide

## What it does

Measure local recovery under service failure. The intended user is reliability learners. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Run python demo.py. It serves from the primary, terminates it, serves from the secondary, restarts the primary, records timings, and cleans up. Start app.py to inspect the resulting report.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Start two real local HTTP processes and wait for readiness before injecting failure.
2. Terminate only the owned primary process and route the next client request to the secondary.
3. Measure failover and restart-to-ready durations with a monotonic clock and always clean up child processes.

## Five interview questions

1. **What failure is injected?** The demonstration starts two owned HTTP subprocesses and terminates the primary. A client then tries the secondary and the primary is restarted.

2. **Where does failover happen?** In sequential client fallback logic. There is no load balancer or DNS change, so it demonstrates a bounded availability mechanism rather than a complete distributed failover system.

3. **What does the recovery timing measure?** Elapsed time for the local experiment’s failure detection, fallback and restart observations. It depends on the machine and request behavior and is not an SLA.

4. **Can you report a recovery point objective?** No. These services are stateless and do not replicate business data. An RPO claim would need a storage and replication model that this project does not have.

5. **How are unrelated processes protected?** The harness manages only subprocesses it created and retains their handles. It does not search for and terminate arbitrary processes by name or port.

## Independent exercise

Add a both-nodes-down case and assert the client reports total unavailability.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Built a reproducible local failure-injection harness that terminates an owned primary HTTP process, measures client fallback and records restart observations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
