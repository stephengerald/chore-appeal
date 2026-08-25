# Security

## Controls reviewed

- The contract pins the concrete GenVM runner `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
- User text, identifiers, arrays, and lifecycle counts are bounded.
- Role and phase checks reject unauthorized or repeated transitions.
- Model input is framed as untrusted evidence; output is restricted to fixed enums or exact-length bitmasks.
- Validator replay recomputes the decision instead of trusting a leader-only answer.
- No private key, wallet file, secret, production credential, token custody, or GEN transfer exists in the repository.

## Threats and limitations

Only on-chain chore requirements, the assignee's claim, and a peer challenge are judged. The contract collects no photos, sensor data, or external source.

Claims can be dishonest and household disputes need human handling. The points are non-monetary signals; do not use this contract for employment or punitive decisions.

On-chain text is public and permanent. Frontends must warn users not to submit secrets, personal identifiers, or confidential evidence. A value-bearing or regulated deployment needs a separate threat model, authenticated sources, operational appeals, and an audited settlement adapter.

Report suspected vulnerabilities privately to the repository owner. Do not place exploit details in a public issue before coordinated review.
