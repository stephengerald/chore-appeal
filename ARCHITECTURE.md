# Architecture

## State machine

The household owner registers members and chores, an assignee claims completion, a different member may challenge, consensus reviews, and the owner finalizes friendly points.

The relevant roles are household owner, assignee, and optional peer challenger. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators interpret a completion claim and challenge against the stored chore standard and return COMPLETE, PARTIAL, or NOT_DONE. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. Claims can be dishonest and household disputes need human handling. The points are non-monetary signals; do not use this contract for employment or punitive decisions.
