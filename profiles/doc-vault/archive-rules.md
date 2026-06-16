# Archive Rules — gc.profile.doc-vault

---

## Archive is not a junk drawer

The `99_archive/` folder is a governed retention zone, not a place to dump old or unwanted files. Every file in the archive must have a reason for being there and must be traceable back to its origin.

---

## Where things go in the archive

### Old drafts → `archive/old-drafts/`

Drafts that were superseded during the review process before execution go here. This includes:

- Draft versions that were replaced by a newer draft
- Drafts from a document that was ultimately abandoned
- Working versions that were merged or restructured before execution

Old drafts are low-sensitivity but must be retained during the document's active lifecycle. After the retention period for the associated executed record expires, old drafts may be destroyed.

### Superseded executed records → `archive/superseded/`

When an executed record is replaced by a new executed version (amendment, restatement, or replacement), the prior executed version moves here. This includes:

- Prior versions of operating agreements
- Prior executed policies
- Replaced contracts or agreements

Superseded executed records retain their original sensitivity and access level. They must be retained for the same retention period as executed records in that category.

---

## Destruction

Records are not deleted without a logged destruction event.

Before destroying any record:

1. Confirm the retention period has expired
2. Confirm no legal hold applies
3. Log the destruction in the destruction log before deleting the file

**Destruction log required fields:**

| date | actor | file | retention_category | reason | notes |

After logging, the file may be permanently deleted. The destruction log entry is the only remaining artifact.

---

## Legal hold prevents all disposition

If a legal hold is active on a record:

- It must not be moved to archive
- It must not be destroyed
- It must not be modified
- Its `legal_hold` flag must remain `true` until a formal written release is issued

Legal hold takes precedence over retention schedule, archive rules, and destruction eligibility.

---

## Archive index

Each archive folder should maintain an archive index tracking:

| original_path | archive_date | reason | superseded_by | retention_category | notes |

This index is the chain-of-custody record for archived materials. It answers:

- Where did this file come from?
- When was it archived?
- Why was it archived?
- What replaced it?
- How long must it be kept?
