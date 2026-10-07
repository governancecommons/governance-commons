# Umbrella release compatibility verification

RFC-0001 A-2 requires release pins to be validated from component compatibility
data. The source is Agent Matrix's `versioning.normative_compatibility` at an
explicit Git commit. The command resolves component release tags to immutable
commits, checks exact Dossier alignment and minimum schema identity, and reports
the evidence used. Runtime and tooling observations do not determine the result.

With the component repositories present beneath this checkout:

```sh
python -m pip install PyYAML==6.0.3 jsonschema==4.26.0
python scripts/validate_release.py releases/gc-v1.2.0.yaml --matrix-ref 478a31db62726cf67822762552b48234e4f9b1db
python -m unittest discover -s tests -p test_release_compatibility.py -v
```

Use `--components` for another directory containing the independent component
checkouts. Verification reads Git objects, so unrelated working-tree changes do
not become compatibility evidence. Missing release tags or compatibility rows
fail verification. The JSON report records resolved commit identities. Preserve
the report with release-review evidence; the command does not modify the manifest.

The historical v1.2.0 manifest currently fails: its `ready_at` field and legacy
`gc_pass_id` do not satisfy the manifest schema, and Dossier v1.1.0 differs from
Matrix v1.4.0's declared v1.0.2 alignment. A newer Dossier version alone does not
prove compatibility. Resolve those contracts through coordinated evidence before
treating the release check as clean. The historical APO entry is ignored by the
specification-compatibility check; future releases reject runtime/tooling entries
in `specs`. Historical release pins and status are preserved.

Git tags establish source availability, not package publication or independent
adoption. ONS release availability and the declared minimum are checked; no
undeclared cross-specification ONS guarantee is inferred. A passing result does
not mark a release ready or activate RFC-0001. Its activation gates remain separate.
