# Hashtag Brews Delivery Contract

## Milestone Workflow

- Work on one approved milestone branch at a time. Do not begin a later milestone until the prior branch is reviewed, merged to `master`, and its gate is accepted.
- Keep each change focused on the active milestone. Record decisions, risks, validation evidence, and deferred work in `PLANS.md` on that branch.
- Before requesting review, run the targeted checks for the milestone and report any checks that could not run.

## Security And Data

- Never commit credentials, tokens, private keys, database passwords, reset links, or generated secrets. Use environment variables or the deployment secret store.
- Treat all authentication, authorization, search, and account-recovery changes as security-sensitive. Add focused tests for access boundaries and invalid input.
- Mutating views must require the appropriate HTTP method, CSRF protection, authentication, and object ownership checks. Return a non-enumerating response for unauthorized objects.

## Application Quality

- Preserve PostgreSQL as the source of truth. Search integrations must be replaceable and must not make normal writes depend on an external search service.
- Meet WCAG AA contrast, keyboard access, visible focus, semantic labels, and usable loading, empty, and error states for user-facing changes.
- Prefer small migrations, reversible rollout steps, and a documented rollback path for data or search changes.

## Gate Checklist

- Clean worktree and focused diff.
- Targeted automated tests pass; run security, dependency, and secret scans when applicable.
- Create an independent, evidence-backed code review in `harness/code_review/phase-XX.md` before requesting each milestone merge. Keep review history append-only and record scope, reviewed commit, findings, resolutions, test evidence, and residual risk.
- A gate cannot pass with an unaccepted P0 or P1 review finding. P2/P3 findings require an explicit resolution or documented deferral approved at the gate.
- Reviewer approval, merge to `master`, and post-merge verification are required before the next milestone begins.
