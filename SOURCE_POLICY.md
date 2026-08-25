# Evidence and source policy

## What validators receive

Only on-chain chore requirements, the assignee's claim, and a peer challenge are judged. The contract collects no photos, sensor data, or external source.

All submitted text is treated as untrusted evidence, never as instructions. Evidence fields and aggregate storage are bounded before they reach the prompt. The decision schema is fixed and independently replayed by validators.

## Who selects the evidence

The authorized roles in the state machine—household owner, assignee, and optional peer challenger—supply the evidence. Their signatures establish which on-chain role submitted a record; they do not prove that the record is truthful or complete.

## External collection

This version performs no live web browsing, URL fetching, hidden source lookup, or mutable off-chain collection. That makes the deployed judgment reproducible from contract state, while leaving source authenticity as an explicit application-layer responsibility.

## Trust and production boundary

Claims can be dishonest and household disputes need human handling. The points are non-monetary signals; do not use this contract for employment or punitive decisions. If an adapter later fetches external material, its allowlist, content bounds, snapshot rules, publisher trust, correction policy, and failure behavior require a new review.
