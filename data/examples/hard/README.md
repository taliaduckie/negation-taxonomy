# Known-hard examples

Each file here holds sentences we believe belong to the type named by the
file, but that the rule-based classifier currently gets wrong. They are run
as strict expected failures: if one starts passing, the test suite will say
so, and the sentence should be promoted to `../<type>.txt`.

Add a sentence here rather than dropping it when it exposes a real gap.
