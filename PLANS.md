# Hashtag Brews Build Plan

## Delivery Ledger

| Milestone | Branch | Status | Gate Evidence |
| --- | --- | --- | --- |
| M0 Delivery Harness | `codex/phase-00-delivery-harness` | In progress | Pending review of `AGENTS.md` and this ledger |
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

- Start each feature branch from the accepted `master` merge commit of the prior milestone. Do not stack unmerged milestone branches.
- Each milestone has exactly one end-of-milestone merge gate. The criteria below are evaluated together at that gate; they do not create additional approvals or phase boundaries.
- Every gate requires a clean worktree, focused diff, targeted tests, applicable security/dependency/secret scans, an independent review record in `harness/code_review/phase-XX.md`, reviewer approval, merge to `master`, and post-merge verification.
- Review records are append-only. No unaccepted P0/P1 finding may cross a gate; P2/P3 findings need an explicit resolution or approved deferral.
- GitHub Actions runs migrations and the deterministic Django test suite against PostgreSQL and Elasticsearch on pull requests and pushes to `master`. Legacy Selenium functional tests move to the M2 browser-modernization acceptance suite.
- The native Google Doc planning brief is created only after the M0 gate is accepted, using this file as its source of truth.

## Deferred Scope

- Public recipe discovery and sharing.
- Vendor inventory, ordering, and brew-day workflow.
- Water chemistry, carbonation, and advanced style-fit scoring.

## M0 Acceptance Evidence

- Branch starts from `master` commit `63a69b45bf80cc58125710baffc49b93bef1153f`.
- Root `AGENTS.md` defines security, quality, and milestone gate requirements.
- Root `PLANS.md` captures branch sequence, product decisions, deferred scope, and gate evidence.
- `harness/code_review/phase-00.md` records the M0 review and establishes the required review format for later phases.
- `.github/workflows/tests.yml` establishes the baseline GitHub Actions test job.
