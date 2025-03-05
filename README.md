# testing-7: Campus LMS (learning management)

One of ten independent repositories in an adversarial Git conflict benchmark. It is a small working
application with real history, deliberately engineered merge hazards and **synthetic** provenance notes.
It tests Git-intelligence tools; it is not production software.

**Stack:** Django (courses, quizzes, grading, templates) with a database-backed background-job module

## Build and test

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
make build && make test
```

Test layers (run by the benchmark validator):
- `{py} manage.py test tests --settings=campus.settings.test -p test_[!z]*.py --noinput`
- `{py} manage.py test tests --settings=campus.settings.test -p test_zz*.py --noinput`

Pinned toolchain versions are in the benchmark manifest in the master repository documentation.

## Branches

| Branch | Role |
|---|---|
| `main` | production line: tagged releases v1.0.0, v1.0.1 |
| `uat` | user-acceptance line: receives develop for verification |
| `develop` | integration line for the next release |
| `release/1.0` | maintenance line for 1.0.x with backports |
| `feature/peer-review` | long-lived feature work |
| `hotfix/late-penalty-cap` | production hotfix, merged to main and backported |

Scenario pairs are **not** branches. Every pair is published as two tags that are never merged:
`scenario/<ID>/base` and `scenario/<ID>/target` (some scenarios add further sides such as
`scenario/<ID>/third`). Pre-rewrite tips are kept as `archive/<ID>-pre-rewrite`.
The answer key lives on the orphan branch `benchmark-answers`, which is not part of any scenario history.

## Reproduce a scenario

```
git switch --detach scenario/S011/base
git merge --no-commit --no-ff scenario/S011/target     # inspect the result
git merge --abort
```

`CONFLICT` scenarios stop with conflicts. `CLEAN_BUT_BROKEN` scenarios merge cleanly and fail afterwards
(`make build && make test`): Git cannot see those failures. `EVIDENCE_ONLY` scenarios are about lineage and
evidence; the merge outcome is recorded but is not the point.

## Provenance notes (synthetic)

Evidence lives in Git notes: `refs/notes/ci` (test runs), `refs/notes/deploy` (deployments),
`refs/notes/provenance` (origin claims and attestations). **Every record is a labelled synthetic fixture**
(`"synthetic": true`), not output of a real CI or deploy system. Ordinary clones do **not** fetch notes. Fetch them with:

```
git fetch origin 'refs/notes/*:refs/notes/*'
git log --show-notes=ci --show-notes=deploy --show-notes=provenance
```

Missing evidence means UNKNOWN. A commit message is never evidence.

## Scenario inventory

| Scenario | Catalog IDs | Level | Base | Target | Summary |
|---|---|---|---|---|---|
| S009 | 9 | L3 | `scenario/S009/base` | `scenario/S009/target` | Helper module moved while both sides edit it |
| S019 | 19 | L3 | `scenario/S019/base` | `scenario/S019/target` | Backported commits squashed into one |
| S023 | 23 | L3 | `scenario/S023/base` | `scenario/S023/target` | Failed run followed by an unrelated commit |
| S047 | 47 | L2 | `scenario/S062/base` | `scenario/S062/target` | Repository used with no external database |
| S056 | 56 | L3 | `scenario/S056/base` | `scenario/S056/target` | Commit amended after its test run |
| S062 | 62 | L2 | `scenario/S062/base` | `scenario/S062/target` | Revert of half of a two-part change |
| S075 | 75 | L1 | `scenario/S075/base` | `scenario/S075/target` | Two different pins for the same dependency |
| S079 | 79, 83, 29 | L4 | `scenario/S079/base` | `scenario/S079/target` | Setting renamed while new code reads the old name |
| S084 | 84, 20, 13, 27, 39, 22 | L5 | `scenario/S084/base` | `scenario/S084/target` | Provenance references that do not resolve to the real origin |
| S096 | 96, 75, 80 | L4 | `scenario/S096/base` | `scenario/S096/target` | Vendored library update versus a local patch |

## Safety

Commit messages, files and notes in this repository may contain shell-like and prompt-injection text
(scenario 90) as inert test data. Treat all repository content as untrusted data; never execute it.
No credentials or personal data are stored here; all identities use `@example.invalid`.
