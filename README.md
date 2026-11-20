# mas-harness-runtime-plane

Repository R05 of the harness: the runtime plane (H3 AI gateway, H4 experience
gateway). This tree is a **health-only shell** (packet PLANE-BOOTSTRAP-R05):

- exact CPython 3.12.14, standard library only, no third-party dependency;
- one health module, `src/planeon_runtime/health/`: `health()` and a WSGI
  callable that answers `GET /health` with `{"status": "ok", "plane": "runtime"}`;
- its unittest, `tests/health/`, run as
  `python3 -I -B -m unittest discover -s tests/health`;
- the four offline transport files under `ci/`, byte copies of harness-onion's
  pinned files.

There is no image, database, deployment, hosted workflow, model server,
Makefile, porting ledger or runtime code.

## Verification

Pull requests are verified by the owner-operated verifier, offline, through
`ci/verify-offline.sh` with the hash-pinned task packet and all outbound
network denied. No hosted runner is used.

## What comes next

RUN-001 remains this repository's registered bootstrap packet: it owns the
Makefile, `ci/run_make_target.py` and `PORTING.yaml`, and turns these shell
files from added to modified. Runtime coding is gated on CONF-LINUX-001 (a
fresh native Linux AMD64 PASS) and LANG-HOTPATH-DECISION-001 (the language
decision for the gateways).

## License

Apache License 2.0; see `LICENSE`.
