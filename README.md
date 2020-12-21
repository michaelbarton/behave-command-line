# behave-command-line

Gherkin steps for steps for testing command line applications using [Behave][].

## How it works

This library creates a [scripttest][] environment in the behave runner context
as an attribute named `env`. When performing command line actions a
[ProcResult][] object is appended to a context attribute `outputs` with the
type `List[ProcResult]`. This can be interogated, examples are on the
documentation in the scripttest website.

[Behave]: https://behave.readthedocs.io/en/stable/
[scripttest]: https://scripttest.readthedocs.io/en/latest/
[ProcResult]:
https://scripttest.readthedocs.io/en/latest/modules/scripttest.html#scripttest.ProcResult
