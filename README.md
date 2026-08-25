# Chore Appeal

Tracks household chores, completion claims, one peer challenge, and friendly deterministic points after consensus review.

## Why GenLayer

Validators interpret a completion claim and challenge against the stored chore standard and return COMPLETE, PARTIAL, or NOT_DONE.

## Reusable workflow

The household owner registers members and chores, an assignee claims completion, a different member may challenge, consensus reviews, and the owner finalizes friendly points. Constructor parameters create a new independent instance, so the code is reusable; state is not shared between deployments.

The contract is deliberately non-custodial. It records a decision, entitlement, score, or approval signal and never transfers GEN.

## Evidence boundary

Only on-chain chore requirements, the assignee's claim, and a peer challenge are judged. The contract collects no photos, sensor data, or external source.

## Verify locally

```powershell
genvm-lint check contracts/chore_appeal.py
genvm-lint typecheck contracts/chore_appeal.py
pytest tests/direct -q
python tests/run_glsim.py --validators 5
```

With GLSim running in another terminal:

```powershell
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The live smoke test requires fresh test-only keys in `GENLAYER_PRIVATE_KEY`, `GENLAYER_SECONDARY_PRIVATE_KEY`, `GENLAYER_TERTIARY_PRIVATE_KEY`. Never commit a `.env` file or use a production wallet.

```powershell
gltest tests/integration/test_studionet_smoke.py --network studionet -s -q --default-wait-interval=6000 --default-wait-retries=240
```

Use the documented 6-second StudioNet polling interval to stay comfortably below public endpoint limits.

See `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md`, and `deployments/studionet.json` for the review boundary and exact public evidence.
