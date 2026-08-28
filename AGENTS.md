# Hashtag Brews Delivery Contract

## Milestone Workflow

- Work on one approved milestone branch at a time. Do not begin a later milestone until the prior branch is reviewed, merged to `main`, and its gate is accepted.
- Keep each change focused on the active milestone. Record decisions, risks, validation evidence, and deferred work in `PLANS.md` on that branch.
- Before requesting review, run the targeted checks for the milestone and report any checks that could not run.

## Review Governance

- Every code-bearing pull request requires an independent staff-level code review.
- Every executable or behavior-affecting change also requires an independent security review. This includes source, tests, scripts, CI, dependencies, configuration, migrations, commands, and operational instructions or snippets that can be executed.
- Before a milestone gate, perform an end-to-end (E2E) phase review of the complete phase diff and its acceptance evidence. This is a delivery review; it does not by itself require browser automation.
- Reviewer separation scales with risk: a low-risk change may use one reviewer in separate code and security passes; complex, security-sensitive, or data-affecting work requires distinct code and security reviewers. Security review remains distinct from the E2E phase review.
- The main task owns every finding disposition: `resolved`, `deferred`, or `cancelled as out of scope`. Do not silently expand scope to address a finding. P0/P1 findings block the gate; P2/P3 deferrals require explicit gate approval.
- Documentation/comments-only pull requests skip these review requirements only when they contain no executable or behavior-affecting content. Embedded commands, scripts, CI snippets, dependency/configuration changes, or operational instructions require security review.

## Security And Data

- Never commit credentials, tokens, private keys, database passwords, reset links, or generated secrets. Use environment variables or the deployment secret store.
- When credentials are found in tracked files, remove them immediately, rotate them in the external system, and document the rotation evidence without recording the secret value.
- Treat all authentication, authorization, search, and account-recovery changes as security-sensitive. Add focused tests for access boundaries and invalid input.
- Mutating views must require the appropriate HTTP method, CSRF protection, authentication, and object ownership checks. Return a non-enumerating response for unauthorized objects.

## Application Quality

- Preserve PostgreSQL as the source of truth. Search integrations must be replaceable and must not make normal writes depend on an external search service.
- Meet WCAG AA contrast, keyboard access, visible focus, semantic labels, and usable loading, empty, and error states for user-facing changes.
- Prefer small migrations, reversible rollout steps, and a documented rollback path for data or search changes.

## Gate Checklist

- Each milestone has exactly one end-of-milestone merge gate. Tests, scans, review, and post-merge verification are acceptance criteria for that single gate, not separate gates.
- Clean worktree and focused diff.
- Targeted automated tests pass; run security, dependency, and secret scans when applicable.
- GitHub Actions must run the deterministic Django test suite for every pull request and push to `main`; browser-driven functional tests remain a separately gated M2 modernization task.
- Create an independent, evidence-backed code review in `harness/code_review/phase-XX.md` before requesting each milestone merge. Keep review history append-only and record scope, reviewed commit, findings, resolutions, test evidence, and residual risk.
- A gate cannot pass with an unaccepted P0 or P1 review finding. P2/P3 findings require an explicit resolution or documented deferral approved at the gate.
- Reviewer approval, merge to `main`, and post-merge verification are required before the next milestone begins.

## Blocker Timeboxes

- For non-core environment, remote-service, credential, third-party, or flaky-infrastructure blockers, use a default two-hour timebox.
- At the timebox limit, stop and report attempts, evidence, impact, options, and a recommendation. Do not extend remote or infrastructure work without a user decision.
- The user may override a timebox for a task or phase in `PLANS.md` or in the conversation.
