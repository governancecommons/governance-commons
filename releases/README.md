# Umbrella release compatibility verification

RFC-0001 A-2 requires release pins to be validated from component compatibility
data. The source is Agent Matrix's `versioning.normative_compatibility` at an
explicit Git commit. The command resolves component release tags to immutable
commits, checks exact Dossier alignment and minimum schema identity, and reports
the evidence used. Runtime and tooling observations do not determine the result.

With the component repositories present beneath this checkout:

```sh
python -m pip install PyYAML==6.0.3 jsonschema==4.26.0
python scripts/validate_release.py releases/gc-v1.2.0.yaml --matrix-ref 296c587da1488c95e17f9627c343f0d67e72211a
python -m unittest discover -s tests -p test_release_compatibility.py -v
```

Use `--components` for another directory containing the independent component
checkouts. Verification reads Git objects, so unrelated working-tree changes do
not become compatibility evidence. Missing release tags or compatibility rows
fail verification. The JSON report records resolved commit identities. Preserve
the report with release-review evidence; the command does not modify the manifest.

The v1.2.0 manifest passes structural and component compatibility validation and
remains `planned`. It retains its original pins and `ready_at` timestamp. Founder
ruling on 2026-10-07 clarifies that `GC-PASS-0015.00` authoritatively identifies
the June 8 PASS-4 gate review; its June 30 reuse was a clerical duplicate with no
separate release-review authority. The historical gate is not treated as a current
GC v1.2.0 release review.

Agent Matrix commit `296c587da1488c95e17f9627c343f0d67e72211a`
establishes bounded compatibility between Dossier v1.1.0 and Matrix v1.4.0. Its
machine-readable evidence pins both release commits and artifact digests and tests
the `dossier-envelope-projection-v1` integration profile. The claim is specification
integration, not schema identity or runtime interoperability. Dossier's divergent
internal version labels are disclosed in that evidence rather than normalized away.

Compatibility validation passing does not restore release readiness. Complete a
current release review and the remaining admission gates before changing the manifest to `ready`.
The schema rejects readiness with unresolved review provenance, missing pins,
non-ok component compatibility, or open holds. The historical APO entry is ignored
by the specification-compatibility check; future releases reject runtime/tooling
entries in `specs`.

Git tags establish source availability, not package publication or independent
adoption. ONS release availability and the declared minimum are checked; no
undeclared cross-specification ONS guarantee is inferred. A passing result does
not mark a release ready or activate RFC-0001. Its activation gates remain separate.
