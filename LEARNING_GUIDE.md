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

1. **What problem does this project solve, and what is its unit of work?** Explain measure local recovery under service failure, identify reliability learners as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Start two real local HTTP processes and wait for readiness before injecting failure. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Terminate only the owned primary process and route the next client request to the secondary. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Measure failover and restart-to-ready durations with a monotonic clock and always clean up child processes. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** Single-host, stateless client-side fallback. No load-balancer process, replicated database, cloud availability-zone failure or data-loss measurement. One local run cannot establish an SLA; RPO is not applicable. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add a both-nodes-down case and assert the client reports total unavailability.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated measure local recovery under service failure using Python · HTTP · SQLite, with two real local http processes and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
