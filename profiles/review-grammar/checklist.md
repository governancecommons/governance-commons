# Review Grammar Adoption Checklist

Status: draft
Profile: gc.profile.review-grammar v0.1.0

Use this checklist for a five-minute adoption check in a development repository.

## Required

- [ ] `docs/REVIEW-GRAMMAR.md` exists.
- [ ] The grammar defines `normalize`.
- [ ] The grammar defines `validate`.
- [ ] The grammar defines `verify`.
- [ ] The grammar defines `adversarial audit`.
- [ ] The grammar defines `meta-audit`.
- [ ] The grammar defines `trace`.
- [ ] The grammar defines `authority audit`.
- [ ] The grammar defines `registry audit`.
- [ ] The grammar defines `close the loop`.
- [ ] The grammar defines `de-stale`.
- [ ] The grammar distinguishes first-order review, meta-audit / second-order review, and process audit / third-order review.
- [ ] The grammar uses closure states: `open`, `spec-complete`, `release-complete`, `runtime-complete`.
- [ ] The grammar requires review outputs to include scope, findings, evidence, validation, and next action.
- [ ] At least one active agent instruction file references `docs/REVIEW-GRAMMAR.md`.

## Recommended

- [ ] `projects.yaml` or equivalent registry points to the review grammar.
- [ ] CI runs `validate-review-grammar.ps1`.
- [ ] Agent instruction files state that review commands must follow the grammar.
- [ ] Review findings cite file paths or evidence.
- [ ] Gap closure distinguishes documented, released, and runtime-enforced states.

## Not Sufficient

- [ ] A repo has a review grammar file but no agent instruction references.
- [ ] A repo uses the words normalize or validate without defining them.
- [ ] A repo calls a gap closed because a document exists.
- [ ] A repo has no way to tell whether the gap tracker itself is stale.
