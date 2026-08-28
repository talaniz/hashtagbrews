# Hashtag Brews Build Plan

## Delivery Ledger

| Milestone | Branch | Status | Gate Evidence |
| --- | --- | --- | --- |
| M0 Delivery Harness | `codex/phase-00-delivery-harness` | Complete | Merged to `main` at `f7bf1fa`; post-merge CI passed |
| Post-M0 Governance | `codex/post-m0-governance` | In progress | Documentation-only governance update; human approval required before merge |
| M1 Security and Accounts | `codex/phase-01-security-accounts` | Blocked by M0 gate | N/A |
| M2 Django Modernization | `codex/phase-02-django-modernization` | Blocked by M1 gate | N/A |
| M3 PostgreSQL Search | `codex/phase-03-postgres-search` | Blocked by M2 gate | N/A |
| M4 Private Recipe MVP | `codex/phase-04-private-recipe-mvp` | Blocked by M3 gate | N/A |
| M5 Modern HTMX UI | `codex/phase-05-modern-htmx-ui` | Blocked by M4 gate | N/A |
| M6 Login Hero and Release | `codex/phase-06-auth-hero-release` | Blocked by M5 gate | N/A |

## Approved Product Direction

- Private recipe-creator MVP: owner-scoped recipes, reusable ingredients, batch and process settings, notes, duplicate/archive/history, and core OG, FG, ABV, IBU, color, and batch-size calculations.
- PostgreSQL native ingredient search replaces Elasticsearch after staged parity validation. The public contract is `IngredientSearchService.search(query, types, filters, sort, page)`.
- Django + HTMX provides the modern responsive application experience. The design handoff includes recipe library, recipe builder, ingredient search, recipe detail, and auth/onboarding screens.
- Authentication includes self-service registration, administrator-created accounts, secure login/logout, and privacy-preserving forgotten-password/reset-password flows.
- The login hero is a photorealistic backyard-wedding beer cheers, framed upward with hands, arms, and glasses only; no faces, logos, text, or watermarks. The interface must preserve form contrast and a usable mobile crop.

## Branch And Gate Policy

- Start each feature branch from the accepted `main` merge commit of the prior milestone. Do not stack unmerged milestone branches.
- Each milestone has exactly one end-of-milestone merge gate. The criteria below are evaluated together at that gate; they do not create additional approvals or phase boundaries.
- Every gate requires a clean worktree, focused diff, targeted tests, applicable security/dependency/secret scans, an independent review record in `harness/code_review/phase-XX.md`, reviewer approval, merge to `main`, and post-merge verification.
- Review records are append-only. No unaccepted P0/P1 finding may cross a gate; P2/P3 findings need an explicit resolution or approved deferral.
- Every code-bearing pull request receives independent staff-level code review. Any executable or behavior-affecting change receives security review; tests, scripts, CI, dependencies, configuration, migrations, commands, and executable operational instructions are in scope.
- Before a milestone gate, an E2E phase review covers the complete phase diff and acceptance evidence. Low-risk work may use the same reviewer for separate code and security passes; complex, security-sensitive, or data-affecting work uses distinct reviewers, and security review remains distinct from E2E phase review.
- Use append-only records named `phase-XX-<title>-code.md`, with `-security.md` and `-e2e.md` where required. The main task records each finding as resolved, deferred, or cancelled as out of scope; no scope expansion is implicit. P0/P1 blocks the gate. P2/P3 deferrals require explicit gate approval.
- Documentation/comments-only pull requests are exempt only when no executable or behavior-affecting content is included. Embedded commands, scripts, CI snippets, dependency/configuration changes, or operational instructions require security review.
- Apply a two-hour default timebox to non-core environment, remote-service, credential, third-party, and flaky-infrastructure blockers. At the limit, stop and report attempts, evidence, impact, options, and a recommendation; extend only with a user decision recorded here or in conversation.
- GitHub Actions runs migrations and the deterministic Django test suite against PostgreSQL and Elasticsearch on pull requests, pushes to `main`, and manually dispatched bootstrap runs. Legacy Selenium functional tests move to the M2 browser-modernization acceptance suite.
- Scope exception: credential removal and automated secret scanning were pulled forward from M1 to unblock the M0 remote CI push. Credential rotation remains an external M1 acceptance action and must be evidenced without recording secret material.
- The native Google Doc planning brief is created only after the M0 gate is accepted, using this file as its source of truth.

## Deferred Scope

- Public recipe discovery and sharing.
- Vendor inventory, ordering, and brew-day workflow.
- Water chemistry, carbonation, and advanced style-fit scoring.

## M0 Acceptance Evidence

- Branch starts from the `main` migration baseline commit `63a69b45bf80cc58125710baffc49b93bef1153f`.
- Root `AGENTS.md` defines security, quality, and milestone gate requirements.
- Root `PLANS.md` captures branch sequence, product decisions, deferred scope, and gate evidence.
- `harness/code_review/phase-00.md` records the M0 review and establishes the required review format for later phases.
- `.github/workflows/tests.yml` establishes the baseline GitHub Actions test job.
- Deprecated Travis configuration and obsolete settings containing tracked credentials are removed; GitHub Actions runs a working-tree secret scan.
- Local test bootstrap is documented with Python 3.9, a project virtual environment, and disposable PostgreSQL 10/Elasticsearch 5.6 services in `docker-compose.test.yml`.
- On 2026-08-28, `homebrewdatabase.tests` and `accounts.tests` passed: 65 tests, 0 failures. The legacy Selenium suite requires Firefox and `geckodriver`; its aggregate-run stability remains an M2 browser-modernization risk.
- Remote CI passed on commit `6518865`: the SHA-pinned Gitleaks scan and Django test jobs both succeeded. The final M0 review has no code/config findings; the gate approver accepted deferral of external credential rotation to M1.
- Legacy Selenium functional tests remain outside GitHub Actions. M2 will baseline their state and choose a modern headless browser-test approach before changing them.
- M0 merged to `main` through pull request #10 on 2026-08-28. Its post-merge GitHub Actions run passed on `f7bf1fa`.
