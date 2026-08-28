# M0 Delivery Harness Review

## Review Scope

- Branch: `codex/phase-00-delivery-harness`
- Reviewed commit range: branch diff against `master` at the M0 merge gate.
- Goal: establish the delivery contract, milestone ledger, phase-review protocol, and baseline GitHub Actions test workflow without application changes.
- Reviewed files: `AGENTS.md`, `PLANS.md`, `harness/code_review/`, `.github/workflows/tests.yml`

## Findings

No blocking review findings.

## Verification

- Passed: `git diff --check` for the M0 diff.
- Passed: clean worktree after the initial M0 commit.

## Residual Risk

- No Markdown-specific lint or repository secret scan was available or run for this documentation/configuration milestone. M1 explicitly adds the required security scanning gate before any security/account code is accepted.
- GitHub Actions cannot be exercised locally; its first remote run after this branch is pushed is required M0 gate evidence.

## Gate Disposition

- Review status: ready for human approval.
- M0 remains unmerged. Do not start M1 until this review and the milestone gate are accepted.

## Addendum: Independent Review After CI Introduction

- Reviewer: Anscombe
- Reviewed head: `e997c32`
- Reviewed scope: full branch diff against `master`, including the GitHub Actions workflow.

### Findings

- [P0] Pre-existing tracked credentials remain in the legacy Travis configuration and an old settings file. These values must be treated as compromised, rotated outside the repository, removed from tracked files, and protected by a secret scan in M1. This finding is not introduced by M0, but prevents the M0 merge gate from passing under the current delivery contract.
- [P1] The initial review record covered an earlier branch state. This addendum records the reviewed head and the CI change; a final addendum must capture the remote GitHub Actions result before M0 can pass.
- [P2] The workflow originally ran on every branch push. Resolved: it now runs on pull requests, pushes to `master`, and explicit `workflow_dispatch` bootstrap runs.
- [P2] The GitHub Actions workflow has not yet run remotely. Open until the manually dispatched branch run succeeds or fails and its result is recorded here.

### Verification

- Passed: `git diff --check`.
- Passed: workflow YAML parse.
- Pending: remote GitHub Actions execution after branch push.

### Gate Disposition

- M0 is blocked by the unresolved P0 credential finding and pending remote CI evidence.
- Pushing this branch for CI observation does not approve, merge, or advance the milestone.

## Addendum: Credential Removal Before Remote CI

- Scope exception approved by the user: pull the tracked credential-removal work forward from M1 before pushing M0.
- Resolved in the working tree: removed the deprecated Travis configuration, its Travis-only database configuration, and the obsolete settings module identified by the independent review as tracked credential sources.
- Added: GitHub Actions working-tree secret scan using Gitleaks for pull requests, pushes to `master`, and manually dispatched runs.
- Open external action: rotate the previously exposed CI/database credentials and record only the rotation completion evidence in the M1 review record. No secret values belong in this repository or review history.
- M0 remains blocked pending the first remote CI run and human gate approval; the M1 security gate remains responsible for validating the external rotation.

## Addendum: Secret Scanner Hardening

- Resolved: the Gitleaks checkout now uses complete Git history so pull-request and pushed-commit scanning can evaluate the relevant commit range.
- Resolved: Gitleaks is pinned to the reviewed immutable `v3.0.0` revision and receives GitHub's ephemeral token for pull-request integration.
- Open: the remote scan is expected to provide the final result for both the current branch and historical credential exposure. Historic remediation remains rotation-first; history rewrite requires separate explicit approval.

## Addendum: Default Branch Migration

- The approved default branch is now `main`, created at the prior `master` baseline commit `63a69b45bf80cc58125710baffc49b93bef1153f`.
- Current delivery-policy and CI references use `main`. Earlier references to `master` in this append-only review record describe the prior branch name at the time of review.
- `master` remains preserved until GitHub's default branch is changed to `main` and the transition is verified.

## Addendum: Local Test Harness Recovery

- Scope exception approved by the user: make the documented test suite runnable before the M0 gate.
- Added a Python 3.9 virtual-environment setup, a disposable PostgreSQL 10/Elasticsearch 5.6 Compose definition, and explicit test settings in `README.md`.
- Updated `psycopg2` from 2.7.3.2 to 2.8.6: the old pin cannot build with Python 3.9; 2.8.6 retains the Django 2.0-compatible timezone behavior.
- The deterministic suite passed on 2026-08-28: `homebrewdatabase.tests` plus `accounts.tests`, 65 tests, 0 failures.
- Firefox functional tests now locate modal controls only after they are visible; an isolated login journey passed. The aggregate Selenium runner still leaves an orphaned browser/database in this environment, so full browser-suite stabilization remains an M2 acceptance item.

## Addendum: First Remote CI Result

- Pull request #10 triggered the first remote `Django tests` workflow run on 2026-08-28.
- Passed: the Gitleaks secret-scan job.
- Failed before checkout: the Django job could not initialize its PostgreSQL service because the unavailable `postgres:10.24` image tag was configured.
- Resolved in the branch: aligned the CI service image with the verified local harness image, `postgres:10`.
- Resolved in the branch: disabled Elasticsearch 5 X-Pack HTTP authentication so the legacy unauthenticated health check and test clients can connect.
- Passed: the head run for `fabd527` completed successfully on 2026-08-28: Gitleaks, service startup, dependency installation, migrations, and Django tests all passed.
- Resolved in the branch: pinned `actions/checkout` and `actions/setup-python` to reviewed immutable SHAs. The fresh head CI result remains required before acceptance.
- Open external action: the owner must confirm rotation of the previously exposed credentials without recording secret material.

## Addendum: Final M0 Review

- Reviewer: Ampere
- Reviewed commit range: `main...6518865`.
- Verification: GitHub Actions run `33217711092` passed on 2026-08-28. The SHA-pinned Gitleaks secret scan and Django unit-test job both succeeded, including service startup, migrations, and tests.
- Findings: no actionable code or configuration P0-P3 findings.
- Residual risk: the previously exposed credentials must be rotated externally. This confirmation must be recorded without secret material before the gate is accepted.
- Gate disposition: code and configuration are ready for M0 approval; merge remains pending the rotation attestation, final human gate approval, merge to `main`, and post-merge verification.
