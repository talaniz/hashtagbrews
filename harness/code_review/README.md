# Phase Code Reviews

Create one append-only review record for every milestone before its merge gate. Name it `phase-XX.md` and include:

- reviewed branch and commit range;
- phase goal and changed files;
- findings ordered by P0 through P3, with file/line evidence and resolution status;
- verification run and anything not run;
- residual risks and approved deferrals; and
- reviewer and gate disposition.

No unaccepted P0 or P1 finding may cross a milestone gate. P2 and P3 findings must be resolved or explicitly deferred by the gate approver.
