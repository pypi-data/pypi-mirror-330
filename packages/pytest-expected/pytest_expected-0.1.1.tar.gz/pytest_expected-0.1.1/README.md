# pytest-expected

This pytest fixture lets you write tests that compare to a previously known, recorded value:

```py
def test_something(expected):
    assert something(frobnicate=True) == expected
```

When called with `--record`, pytest will accept any value and store it in a
file in the hidden `.expected` directory under the pytest root folder (usually
the repository root).

When called _without_ `--record`, it will load the known value(s) from that
store, and assert that they are equal to the observed values.

Any picklable value can be stored.

You can also use `expected` several times in a test for different values, and
it'll figure out the rest.

`pytest-expected` organizes storage based on:

- Test ID (typically includes path to test file, test name, and parametrizations)
- Number of uses of `expected`
