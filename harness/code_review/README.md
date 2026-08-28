# Phase Code Reviews

Create append-only review records for every milestone before its merge gate. Use `phase-XX-<title>-code.md` for the independent staff code review, plus `phase-XX-<title>-security.md` for executable or behavior-affecting changes and `phase-XX-<title>-e2e.md` for the complete phase-gate review. A low-risk change may use one reviewer in separate code and security passes; complex, security-sensitive, or data-affecting work requires distinct code and security reviewers. Security review remains distinct from E2E phase review.

Documentation/comments-only pull requests may skip these records only when they have no executable or behavior-affecting content. Embedded commands, scripts, CI snippets, dependency/configuration changes, or operational instructions require a security record.

Every record must include:

- reviewed branch and commit range;
- phase goal and changed files;
- findings ordered by P0 through P3, with file/line evidence and disposition (`resolved`, `deferred`, or `cancelled as out of scope`);
- verification run and anything not run;
- residual risks and approved deferrals; and
- reviewer and gate disposition.

The main task owns finding disposition and must not silently expand scope. No unaccepted P0 or P1 finding may cross a milestone gate. P2 and P3 findings must be resolved, cancelled as out of scope, or explicitly deferred by the gate approver.

For an E2E phase record, include the whole phase diff, all required code/security records, acceptance evidence, and post-merge plan. If a non-core environment, remote-service, credential, third-party, or flaky-infrastructure blocker reaches its two-hour default timebox, record attempts, evidence, impact, options, and a recommendation. Extension requires a user decision in `PLANS.md` or conversation.
